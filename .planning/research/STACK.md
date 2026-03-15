# Stack Research

**Domain:** Healthcare AI / Real-time Anomaly Detection
**Researched:** 2025-05-15
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **Python** | 3.12+ | Primary Runtime | Latest stable version offering superior performance (Faster CPython) and modern type hinting, critical for complex ML pipelines. |
| **Apache Kafka** | 3.7+ (KRaft) | Event Streaming | Industry standard for decoupling high-frequency medical sensors from processing logic. KRaft mode simplifies deployment by removing Zookeeper dependency. |
| **PostgreSQL** | 16+ | Relational Storage | Robust, ACID-compliant "System of Record" for patient metadata and clinical audit trails. Supports advanced indexing for fast retrieval. |
| **TimescaleDB** | 2.14+ (PG Ext) | Time-Series Optimization | Essential Postgres extension for handling massive streams of vitals (EKG, SpO2) with efficient compression and time-bucketed queries. |
| **PyTorch** | 2.3+ | Deep Learning Engine | Preferred for Autoencoders due to its dynamic graph nature and the **MONAI** ecosystem (Medical Open Network for AI) for healthcare-specific data. |
| **Flask** | 3.0.x | Backend API / Web | Lightweight and extensible. In 2025, Flask 3.x remains the standard for specialized microservices where low overhead is prioritized over "batteries-included" frameworks. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **Scikit-learn** | 1.4+ | Classical ML | Use for the **Isolation Forest** implementation and standard preprocessing (scaling, PCA). |
| **Confluent-Kafka**| 2.4+ | Kafka Client | High-performance Python wrapper for `librdkafka`, used for all producer/consumer logic. |
| **SQLAlchemy** | 2.0+ | Modern ORM | Use for type-safe interactions with PostgreSQL and managing complex clinical schemas. |
| **Pydantic** | 2.7+ | Data Validation | Critical for enforcing strict data contracts on incoming vitals and ensuring FHIR compliance. |
| **Pandas** | 2.2+ | Data Wrangling | Use for complex vector-based operations and windowing functions on patient data streams. |
| **React** | 18/19 | Dashboard UI | Recommended for the "Interactive Dashboard" to handle real-time state updates (vitals charts) more efficiently than server-side rendering. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **Docker / K8s** | Containerization | Standard for ensuring "run anywhere" reliability across hospital environments. |
| **Prometheus** | Monitoring | Use to track Kafka lag and inference latency (critical for life-safety systems). |
| **Ruff** | Linting/Formatting | Extreme performance linter/formatter to maintain code quality in fast-moving ML projects. |

## Installation

```bash
# Core Dependencies
pip install flask==3.0.3 torch==2.3.0 scikit-learn==1.4.2 psycopg2-binary==2.9.9

# Streaming & DB
pip install confluent-kafka==2.4.0 sqlalchemy==2.0.30 timescaledb-python

# Supporting & Validation
pip install pydantic==2.7.1 pandas==2.2.2 hfhir
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| **Flask 3.x** | **FastAPI** | Use if high concurrency (asynchronous IO) is the primary bottleneck, though Flask is often preferred for simpler, stable dashboards. |
| **PostgreSQL** | **MongoDB** | Use only if patient data is highly unstructured and schema-on-read is more important than clinical auditability. |
| **PyTorch** | **TensorFlow** | Use if the target hardware has specific optimizations for TFLite (e.g., edge medical devices). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **Python < 3.10** | End-of-life or lacking performance/security patches for 2025. | **Python 3.12+** |
| **Redis (as Primary)** | Volatile by nature; lacks the complex query and archival capabilities needed for medical history. | **PostgreSQL + TimescaleDB** |
| **Manual Threading** | Risk of race conditions in real-time streams; Kafka handles parallelism better. | **Kafka Consumer Groups** |
| **Raw SQL** | High risk of SQL injection and brittle migrations in healthcare systems. | **SQLAlchemy 2.0** |

## Stack Patterns by Variant

**If High-Frequency (ICU) Monitoring:**
- Use **NVIDIA Triton Inference Server** to serve PyTorch models.
- Because it offloads GPU inference from the Flask app, reducing latency to sub-10ms.

**If Low-Resource/Edge Monitoring:**
- Use **TorchScript** or **ONNX** export for models.
- Because it allows models to run on mobile or embedded devices without a full Python/PyTorch runtime.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| **PyTorch 2.3** | **CUDA 12.1+** | Ensure GPU drivers match for accelerated inference. |
| **Flask 3.0** | **Werkzeug 3.0** | Direct dependency; avoid pinning older Werkzeug. |
| **SQLAlchemy 2.0** | **Psycopg2 2.9** | Required for modern Postgres 16 features. |

## Sources

- [Apache Kafka Documentation] — KRaft mode deployment patterns.
- [PyTorch Healthcare Tutorials] — MONAI integration and Autoencoder architectures.
- [TimescaleDB Blog] — Benchmarking vitals storage in Postgres.

---
*Stack research for: Healthcare Anomaly Detection*
*Researched: 2025-05-15*
