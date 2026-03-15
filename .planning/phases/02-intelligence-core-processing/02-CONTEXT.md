# Phase 2: Intelligence & Core Processing - Context

**Gathered:** March 15, 2026
**Status:** In progress

<domain>
## Phase Boundary

This phase implements the "brain" of the Anomaly Detection System. It moves from raw data persistence (Phase 1) to actionable intelligence. This involves building the machine learning models (Autoencoder and Isolation Forest) and the real-time preprocessing logic that feeds them. It ends when the system can compute anomaly scores and assign severity levels (LOW, MEDIUM, HIGH) for every incoming vital sign packet.

</domain>

<decisions>
## Implementation Decisions

### Machine Learning Models
- **Autoencoder (Neural Network)**: Use PyTorch to build a deep autoencoder. High reconstruction error will signal "out-of-distribution" (unseen) patterns.
- **Isolation Forest**: Use Scikit-learn for this ensemble-based anomaly detection to handle outliers and provide a robust baseline.
- **Ensemble Logic**: Combine scores from both models (e.g., weighted average or max) to determine final severity.

### Preprocessing & Normalization
- **Scaling**: Use `StandardScaler` or `MinMaxScaler` for normalization, fitted on "normal" synthetic data.
- **Noise Filtering**: Implement a simple moving average or median filter to handle sensor noise before inference.

### Model Persistence
- **Format**: Save PyTorch models as `.pt` or `.pth` and Scikit-learn models using `joblib` or `pickle`.
- **Location**: Store model artifacts in a `models/` directory (versioned).

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/scripts/generate_synthetic_data.py`: Can be adapted to create "training" vs "test" (anomalous) datasets.
- `requirements.txt`: Already includes `torch`, `scikit-learn`, `pandas`, and `numpy`.

### Integration Points
- **Inference Service**: Needs to be integrated into the `src/ingestion/worker.py` (or a separate processing service) to score data before it's saved to the DB.
- **Database**: The `vitals` table already has an `anomaly_score` column, and the `anomalies` table is ready for event-based logs.

</code_context>

<specifics>
## Specific Ideas
- Implement a "training mode" script that can be run to refresh models on the latest "normal" data.
- Use a dedicated `InferenceEngine` class to encapsulate model loading and scoring logic.

</specifics>

<deferred>
## Deferred Ideas
- Online/Incremental learning (learning from new data in real-time).
- Advanced signal processing (e.g., Wavelet transforms).

</deferred>

---

*Phase: 02-intelligence-core-processing*
*Context gathered: March 15, 2026*
