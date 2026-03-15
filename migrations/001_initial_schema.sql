-- Enable TimescaleDB extension (already installed in the container but ensuring it's active in the DB)
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Vitals table: High-frequency physiological data
CREATE TABLE IF NOT EXISTS vitals (
    time TIMESTAMPTZ NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    anomaly_score DOUBLE PRECISION DEFAULT 0.0,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

-- Convert to hypertable with 1-day chunk interval
SELECT create_hypertable('vitals', 'time', chunk_time_interval => INTERVAL '1 day', if_not_exists => TRUE);

-- Anomalies table: Event-based detection history
CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    time TIMESTAMPTZ NOT NULL,
    patient_id VARCHAR(50) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    severity VARCHAR(10) CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH')),
    score DOUBLE PRECISION NOT NULL,
    details JSONB,
    received_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alerts table: Notification history
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    anomaly_id INTEGER REFERENCES anomalies(id),
    patient_id VARCHAR(50) NOT NULL,
    alert_time TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'SENT', 'FAILED')),
    received_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_vitals_patient_id ON vitals (patient_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_anomalies_patient_id ON anomalies (patient_id, time DESC);
