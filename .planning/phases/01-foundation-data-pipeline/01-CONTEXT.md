# Phase 1: Foundation & Data Pipeline - Context

**Gathered:** March 15, 2026
**Status:** Ready for planning

<domain>
## Phase Boundary

This phase delivers the core data infrastructure for the AI-Driven Healthcare Anomaly Detection System. This includes the Apache Kafka cluster for real-time ingestion and the PostgreSQL/TimescaleDB instance for optimized clinical time-series storage. It completes the path from "data received" to "data persisted with audit trail."

</domain>

<decisions>
## Implementation Decisions

### Data Ingestion (Kafka)
- **Topic Naming**: Use `patient-vitals-raw` for incoming streams.
- **Partitioning**: Partition by `patient_id` to ensure ordered processing of a single patient's vitals.
- **Retention**: 7-day retention for raw vitals on Kafka to allow for reprocessing if needed.

### Persistence (PostgreSQL/TimescaleDB)
- **Schema**: Separate tables for `vitals` (high frequency), `anomalies` (event-based), and `alerts` (notification history).
- **TimescaleDB**: Use hypertables for the `vitals` table with a 1-day chunk interval for optimal performance and compression.
- **Audit Trail**: Every record in `vitals`, `anomalies`, and `alerts` will include a `received_at` and `processed_at` timestamp for compliance.

### Claude's Discretion
- **Kafka Client Library**: Choice of Python library (e.g., confluent-kafka vs kafka-python) is left to implementation based on performance research.
- **Connection Pooling**: Implementation of DB connection pooling (e.g., SQLAlchemy/psycopg2-pool) is at Claude's discretion.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- None (Greenfield project)

### Established Patterns
- None (First phase)

### Integration Points
- This phase establishes the foundation that all subsequent ML (Phase 2) and API/Dashboard (Phase 3) components will integrate with.

</code_context>

<specifics>
## Specific Ideas
- Use a synthetic data generator script for initial testing of the Kafka-to-DB pipeline before real sensor data is available.
- Ensure the PostgreSQL instance is configured with SSL for clinical data security.

</specifics>

<deferred>
## Deferred Ideas
- ML model integration (Phase 2)
- Real-time dashboard UI (Phase 3)
- Email notification logic (Phase 3)

</deferred>

---

*Phase: 01-foundation-data-pipeline*
*Context gathered: March 15, 2026*
