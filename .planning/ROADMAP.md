# Roadmap: AI-Driven Healthcare Anomaly Detection System

## Phase 1: Foundation & Data Pipeline
**Goal:** Establish Kafka ingestion and Postgres/TimescaleDB storage.

### Success Criteria
- [ ] Kafka cluster is operational and handles high-frequency message streams.
- [ ] PostgreSQL with TimescaleDB is configured for efficient time-series storage.
- [ ] Data ingestion consumer successfully persists incoming vitals to the database.

### Requirements Mapped
- **STREAM-01**: Low-latency ingestion of high-frequency vital signs via Apache Kafka.
- **STREAM-02**: Decoupled consumer architecture.
- **DB-01**: Secure storage of patient vitals and scores in PostgreSQL.
- **DB-02**: Clinical audit trail of anomalies and alerts.
- **DB-03**: Optimized storage using TimescaleDB.

### Proposed Plans
- **Infrastructure Setup**: Deploy Kafka and PostgreSQL with TimescaleDB extension.
- **Schema Design**: Create clinical-grade schemas for vitals, alerts, and audit logs.
- **Ingestion Development**: Build the initial consumer for Kafka-to-DB persistence.

---

## Phase 2: Intelligence & Core Processing
**Goal:** Implement Autoencoder and Isolation Forest models with real-time scoring.

### Success Criteria
- [ ] Autoencoder and Isolation Forest models are implemented and trained.
- [ ] Preprocessing pipeline successfully filters sensor noise in real-time.
- [ ] Real-time anomaly scores are computed and severity levels are assigned correctly.

### Requirements Mapped
- **ML-01**: Autoencoder Neural Network implementation.
- **ML-02**: Isolation Forest implementation.
- **ML-03**: Real-time noise filtering and preprocessing.
- **ML-04**: Real-time anomaly score computation.
- **ML-05**: Severity classification (LOW, MEDIUM, HIGH).

### Proposed Plans
- **Model Development**: Implement unsupervised ML models for detection.
- **Real-time Inference**: Integrate scoring logic into the data processing stream.
- **Preprocessing Engine**: Build signal quality filtering to minimize false positives.

---

## Phase 3: Monitoring & Alerting
**Goal:** Build Flask dashboard, APIs, and email notification system.

### Success Criteria
- [ ] Flask REST APIs serve real-time and historical monitoring data.
- [ ] Dashboard visualizes anomaly trends and highlights active alerts.
- [ ] HIGH-severity anomalies trigger immediate, reliable email notifications.

### Requirements Mapped
- **API-01**: Flask REST APIs for monitoring data.
- **API-02**: Interactive web dashboard.
- **API-03**: Prominent display of active alerts.
- **ALERT-01**: Automated email notification for HIGH-severity alerts.
- **ALERT-02**: Alert logging for delivery reliability.

### Proposed Plans
- **API Development**: Create endpoints for clinical data retrieval.
- **Dashboard Interface**: Build the UI for real-time patient monitoring.
- **Alerting Service**: Integrate an automated notification system for critical events.
