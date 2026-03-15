import os
import time
import json
from datetime import datetime, timezone
from confluent_kafka import Consumer, KafkaError
from psycopg import connect
from dotenv import load_dotenv

load_dotenv()

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC_RAW = os.getenv("KAFKA_TOPIC_RAW", "patient-vitals-raw")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vitals?sslmode=require")
BATCH_SIZE = int(os.getenv("INGESTION_BATCH_SIZE", "100"))
FLUSH_INTERVAL_SEC = float(os.getenv("INGESTION_FLUSH_INTERVAL_SEC", "1.0"))

def ingest_vitals():
    """Consume vitals from Kafka and persist to TimescaleDB."""
    
    # Kafka Consumer Setup
    conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "vitals-ingestion-worker",
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False
    }
    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC_RAW])
    
    print(f"Ingestion worker started. Listening on {KAFKA_TOPIC_RAW}...")

    batch = []
    last_flush_time = time.time()

    try:
        with connect(DATABASE_URL) as conn:
            while True:
                msg = consumer.poll(0.1)
                
                if msg is not None:
                    if msg.error():
                        if msg.error().code() != KafkaError._PARTITION_EOF:
                            print(f"Consumer error: {msg.error()}")
                    else:
                        try:
                            data = json.loads(msg.value().decode("utf-8"))
                            # Add audit trail metadata
                            data["received_at"] = datetime.now(timezone.utc).isoformat()
                            batch.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Failed to decode message: {e}")

                # Flush batch if size reached or time interval elapsed
                if len(batch) >= BATCH_SIZE or (time.time() - last_flush_time >= FLUSH_INTERVAL_SEC and batch):
                    flush_batch(conn, batch)
                    consumer.commit()
                    batch = []
                    last_flush_time = time.time()

    except Exception as e:
        print(f"Worker fatal error: {e}")
    finally:
        consumer.close()

def flush_batch(conn, batch):
    """Bulk insert vitals using the PostgreSQL COPY protocol."""
    processed_at = datetime.now(timezone.utc)
    
    # Prepare data for COPY (CSV-like format)
    rows = []
    for item in batch:
        rows.append((
            item.get("time"),
            item.get("patient_id"),
            item.get("sensor_type"),
            item.get("value"),
            item.get("anomaly_score", 0.0),
            item.get("received_at"),
            processed_at
        ))

    with conn.cursor() as cur:
        with cur.copy("COPY vitals (time, patient_id, sensor_type, value, anomaly_score, received_at, processed_at) FROM STDIN") as copy:
            for row in rows:
                copy.write_row(row)
        conn.commit()
    print(f"Flushed {len(batch)} records to vitals table.")

if __name__ == "__main__":
    ingest_vitals()
