# Phase 1 Research: Foundation & Data Pipeline

## Infrastructure Strategy

### Containerization & Orchestration
- **Docker Compose**: Recommended for local development to ensure parity between dev and future staging environments.
- **Kafka (KRaft Mode)**: Use Apache Kafka 3.7+ in KRaft mode to eliminate Zookeeper dependency, simplifying the infrastructure.
- **PostgreSQL 16 + TimescaleDB**: Use the official `timescale/timescaledb:latest-pg16` image.

### Versioning & Compatibility
- **Python**: 3.12+ for performance and modern type-hinting.
- **Postgres Driver**: `psycopg` (v3) is preferred over `psycopg2` for its improved performance and native async support.
- **Kafka Client**: `confluent-kafka` is the industry standard for performance (C-based `librdkafka` wrapper).

## Database Schema Design

### Vital Signs (Time-Series)
A "wide" table approach is recommended as sensors (e.g., pulse oximeters) often report related metrics (Heart Rate, SpO2) simultaneously.

```sql
CREATE TABLE patient_vitals (
    time            TIMESTAMPTZ NOT NULL,
    patient_id      UUID NOT NULL,
    heart_rate      INTEGER,
    spo2            NUMERIC(5,2),
    temperature     NUMERIC(4,2),
    blood_pressure_sys INTEGER,
    blood_pressure_dia INTEGER,
    received_at     TIMESTAMPTZ DEFAULT NOW(),
    processed_at    TIMESTAMPTZ
);

-- Convert to Hypertable (1-day chunks)
SELECT create_hypertable('patient_vitals', 'time', chunk_time_interval => INTERVAL '1 day');

-- Enable Compression
ALTER TABLE patient_vitals SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'patient_id',
    timescaledb.compress_orderby = 'time DESC'
);
```

### Anomalies & Alerts (Event-Based)
Standard relational tables are sufficient for these lower-frequency events.
- **`anomalies`**: Stores the output of ML models (Phase 2).
- **`alerts`**: Stores notification history and severity (Phase 3).

## Kafka Ingestion Architecture

### Consumer Loop Pattern
To ensure "At-Least-Once" delivery and high throughput:
1. **Poll**: Gather a batch of messages from `patient-vitals-raw`.
2. **Transform**: Deserialization (JSON) and light validation.
3. **Buffer**: Store in an in-memory list.
4. **Flush**: Once the buffer reaches 1,000 records or 5 seconds pass, use the `COPY` protocol to persist to TimescaleDB.
5. **Commit**: Commit the DB transaction, then commit the Kafka offsets.

### Performance Tuning
- **`max_poll_records`**: Set to 1,000 to match DB batch size.
- **Serialization**: Use `orjson` in Python for significantly faster JSON parsing than the standard `json` library.

## Audit & Compliance

### Timestamps
Three distinct timestamps are required for clinical audit trails:
1. **`time`**: The actual physiological event time (from sensor).
2. **`received_at`**: When the record reached the Kafka ingestion layer.
3. **`processed_at`**: When the record was successfully persisted to the DB.

### Security
- **SSL/TLS**: All connections between the Python consumer and PostgreSQL/Kafka must use SSL.
- **Credentials**: Managed via environment variables (`.env`).

## Testing & Synthetic Data

### Synthetic Generator
A dedicated script is needed to simulate patient vitals. It should:
- Support multiple `patient_id` values.
- Simulate realistic physiological ranges (e.g., HR 60-100).
- Introduce occasional "out-of-bounds" values to test future anomaly detection.
- Produce data at a configurable frequency (e.g., 1Hz per patient).

## Planning Checklist
- [ ] Docker Compose file with Kafka (KRaft) and TimescaleDB.
- [ ] DDL scripts for `patient_vitals`, `anomalies`, and `alerts`.
- [ ] Python Project Setup (Poetry/Pip, `confluent-kafka`, `psycopg`).
- [ ] Ingestion Worker logic with batching and `COPY` support.
- [ ] Synthetic data generator for E2E validation.
