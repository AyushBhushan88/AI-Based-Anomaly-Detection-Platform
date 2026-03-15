import pytest
import time
import subprocess
import os
from psycopg import connect

def test_full_ingestion_pipeline(db_connection, kafka_bootstrap_servers):
    """End-to-end test: synthetic data -> Kafka -> Worker -> DB."""
    topic = os.getenv("KAFKA_TOPIC_RAW", "patient-vitals-raw")
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vitals?sslmode=require")

    # Clear table
    with db_connection.cursor() as cur:
        cur.execute("TRUNCATE TABLE vitals;")
        db_connection.commit()

    # Start Worker in background
    worker_proc = subprocess.Popen(
        [".venv/bin/python3", "src/ingestion/worker.py"],
        env={**os.environ, "INGESTION_BATCH_SIZE": "5", "INGESTION_FLUSH_INTERVAL_SEC": "0.1"}
    )

    # Run synthetic generator for a few seconds
    try:
        gen_proc = subprocess.Popen(
            [".venv/bin/python3", "src/scripts/generate_synthetic_data.py"],
            env={**os.environ}
        )
        time.sleep(5)
        gen_proc.terminate()
        time.sleep(2) # Wait for worker to flush
    finally:
        worker_proc.terminate()

    # Verify data in DB
    with db_connection.cursor() as cur:
        cur.execute("SELECT count(*) FROM vitals;")
        count = cur.fetchone()[0]
        assert count > 0, "No data found in vitals table after ingestion"
        
        cur.execute("SELECT patient_id, sensor_type, value, received_at, processed_at FROM vitals LIMIT 1;")
        row = cur.fetchone()
        assert row[0].startswith("PATIENT-")
        assert row[3] is not None, "received_at (audit trail) is missing"
        assert row[4] is not None, "processed_at (audit trail) is missing"
