# AI-Driven Healthcare Anomaly Detection System

## What This Is

An end-to-end real-time monitoring and decision-support platform designed to detect abnormal patterns in patient vital signs and generate early health risk alerts. It continuously analyzes live physiological data streams using machine learning models to identify anomalies as they occur, providing healthcare providers with actionable insights before critical incidents happen.

## Core Value

Detect anomalies in real-time patient vitals to provide early health risk alerts for proactive medical intervention.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Load and integrate anomaly detection models (Autoencoder and Isolation Forest)
- [ ] Preprocess incoming vitals and compute anomaly scores in real time
- [ ] Classify patient health conditions into LOW, MEDIUM, and HIGH severity levels
- [ ] Store patient vitals, anomaly scores, and severity details in PostgreSQL
- [ ] Develop Flask-based APIs to serve real-time and historical monitoring data
- [ ] Build an interactive dashboard to visualize vitals, anomalies, and alerts
- [ ] Trigger automated email notifications for HIGH-severity health anomalies

### Out of Scope

- [Direct device integration] — Focus is on processing data streams (ingestion via Kafka), not hardware-level integration
- [Full Electronic Health Record (EHR) system] — The system is specialized for anomaly detection and alerting, not general patient record management

## Context

The system addresses the limitations of traditional healthcare monitoring that relies on static thresholds. By using machine learning (Autoencoders and Isolation Forests), it can detect subtle deviations in vitals that might indicate a developing health risk. The architecture leverages real-time streaming for immediate processing.

## Constraints

- **Tech Stack**: Apache Kafka — Required for real-time data streaming and ingestion
- **Tech Stack**: PostgreSQL — Primary relational database for historical data and alert storage
- **Tech Stack**: Flask — Backend API and dashboard framework
- **Domain**: Healthcare — Requires high reliability and clear severity classification

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Autoencoder and Isolation Forest | Complementary ML models for identifying complex and diverse anomaly patterns | — Pending |
| Use Apache Kafka for ingestion | Industry standard for reliable, high-throughput real-time data streaming | — Pending |
| Severity-based classification (LOW, MEDIUM, HIGH) | Provides immediate triage capability for healthcare responders | — Pending |

---
*Last updated: March 15, 2026 after initialization*
