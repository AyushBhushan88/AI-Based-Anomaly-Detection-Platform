# Architecture: AI-Driven Healthcare Anomaly Detection System

## 1. System Overview
The AI-Driven Healthcare Anomaly Detection System is a real-time monitoring platform designed to ingest high-velocity physiological data (vitals), process it using unsupervised machine learning models, and provide clinical decision support through alerts and visualizations.

The architecture follows a **streaming-first approach** (Kappa-like) to ensure low-latency detection of life-threatening events.

## 2. Component Boundaries
The system is divided into five primary functional blocks:

### A. Data Ingestion Layer (Kafka)
- **Role:** Acts as the high-throughput buffer for incoming patient vitals.
- **Interfaces:** Receives data from external simulation/stream sources; provides data to the Processing Layer.
- **Boundaries:** Decouples the data sources from the processing logic, ensuring system resilience.

### B. Processing & Analytics Layer (Flask/Python)
- **Role:** Consumes raw vitals from Kafka, performs real-time preprocessing (normalization, windowing), and executes ML inference.
- **Interfaces:** Reads from Kafka; calls ML Models; writes results to PostgreSQL; triggers Alerts.
- **Boundaries:** This is the "brain" of the system where business logic and model orchestration reside.

### C. Intelligence Layer (ML Models)
- **Role:** Contains the pre-trained **Autoencoder** and **Isolation Forest** models.
- **Interfaces:** Receives feature vectors from the Processing Layer; returns anomaly scores and reconstruction errors.
- **Boundaries:** Encapsulated as model objects or microservices to allow independent updates/retraining.

### D. Persistence Layer (PostgreSQL)
- **Role:** Stores historical vitals, computed anomaly scores, and alert logs.
- **Interfaces:** Receives writes from the Processing Layer; serves reads to the Dashboard/API.
- **Boundaries:** Ensures data durability and enables longitudinal patient analysis.

### E. Presentation & Alerting Layer (Flask Dashboard + Email)
- **Role:** Visualizes real-time status and historical trends; sends notifications for HIGH-severity events.
- **Interfaces:** Reads from PostgreSQL/API; interacts with external Email SMTP.
- **Boundaries:** The user-facing interface for clinicians and administrators.

---

## 3. Data Flow
The following flow describes the path of a single vital sign packet:

1.  **Ingestion:** Raw vitals (Heart Rate, SpO2, Blood Pressure) are pushed into a **Kafka Topic** (e.g., `patient-vitals`).
2.  **Streaming:** The **Processing Engine** (Kafka Consumer) pulls the latest messages.
3.  **Pre-processing:** Data is cleaned (handling nulls) and normalized to a scale suitable for the ML models.
4.  **Anomaly Detection:** 
    - The vector is passed to the **Autoencoder**. High reconstruction error indicates a deviation from "normal" patterns.
    - The vector is passed to the **Isolation Forest**. Isolation depth determines how "outlying" the data point is.
5.  **Classification:** Scores are aggregated and mapped to severity:
    - **LOW:** Normal variation.
    - **MEDIUM:** Subtle deviation (warning).
    - **HIGH:** Critical anomaly (urgent alert).
6.  **Persistence:** The vitals, scores, and severity are saved to **PostgreSQL**.
7.  **Alerting:** If severity is **HIGH**, an automated **Email Alert** is triggered.
8.  **Visualization:** The **Flask Dashboard** polls the database/API to update real-time charts.

---

## 4. Suggested Build Order (Dependencies)
To ensure a logical progression where each component has its dependencies met, the following build order is recommended:

1.  **Foundation (Infrastructure):**
    - Set up **PostgreSQL** schema for vitals and alerts.
    - Initialize **Apache Kafka** and define required topics.
2.  **Intelligence (ML Models):**
    - Develop and save the **Autoencoder** and **Isolation Forest** model artifacts using synthetic or historical healthcare datasets.
3.  **Processing (Ingestion & Analysis):**
    - Build the Kafka Consumer/Processor to ingest data, run preprocessing, and perform ML inference.
    - Implement the logic to write results to PostgreSQL.
4.  **Alerting (Communication):**
    - Build the notification service to trigger emails based on HIGH-severity events.
5.  **Dashboard (Visualization):**
    - Develop the Flask API to serve data from PostgreSQL.
    - Build the interactive frontend dashboard to display real-time and historical data.

---

## 5. Deployment Considerations
- **Reliability:** Kafka ensures no data loss during processing spikes.
- **Privacy:** Data in PostgreSQL and transit should be encrypted (standard for HIPAA compliance).
- **Scalability:** The processing layer can be scaled horizontally by adding more Kafka consumer instances.
