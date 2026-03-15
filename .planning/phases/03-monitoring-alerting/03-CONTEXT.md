# Phase 3: Monitoring & Alerting - Context

**Gathered:** March 16, 2026
**Status:** In progress

<domain>
## Phase Boundary

This is the final phase of the project, focusing on the consumption and visualization of the intelligence generated in Phase 2. It moves from background data processing to user-facing applications. This involves building a Flask-based REST API to serve patient vitals and anomaly history, an interactive dashboard for clinical monitoring, and an automated alerting service for critical events. The phase ends when a clinician can view real-time data on a UI and receive email notifications for HIGH-severity anomalies.

</domain>

<decisions>
## Implementation Decisions

### API Layer
- **Framework**: Flask (Python) for a lightweight and flexible REST API.
- **Endpoints**:
    - `GET /api/vitals/<patient_id>`: Historical vitals with anomaly scores.
    - `GET /api/anomalies`: Active and past anomaly events.
    - `GET /api/patients`: List of active patients being monitored.
- **Security**: Implement basic API key or JWT if required (placeholder for now).

### Monitoring Dashboard
- **Technology**: React (TypeScript) with Vanilla CSS (as per project defaults) or a simple Flask-rendered template with Chart.js for the prototype.
- **Visuals**: Real-time line charts for vitals and a "high-alert" sidebar for active anomalies.

### Alerting Service
- **Notification**: Email via SMTP (or a mock service like Mailtrap for development).
- **Trigger**: Only `HIGH` severity anomalies from the `anomalies` table.
- **Reliability**: Use the `alerts` table to track notification status (PENDING, SENT, FAILED).

</decisions>

<code_context>
## Existing Code Insights

### Database
- `vitals` table (TimescaleDB) is populated with scores.
- `anomalies` table tracks detected events.
- `alerts` table is ready for notification logs.

### Requirements
- **API-01, API-02, API-03**: Dashboard and REST APIs.
- **ALERT-01, ALERT-02**: Email notifications and logging.

</code_context>

<specifics>
## Specific Ideas
- Use SSE (Server-Sent Events) or simple polling for "real-time" dashboard updates.
- Create a dedicated `AlertingWorker` that polls the `anomalies` table for unsent high-severity alerts.

</specifics>

---

*Phase: 03-monitoring-alerting*
*Context gathered: March 16, 2026*
