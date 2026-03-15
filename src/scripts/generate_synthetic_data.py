import os
import time
import json
import random
from datetime import datetime, timezone
from confluent_kafka import Producer
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC_RAW = os.getenv("KAFKA_TOPIC_RAW", "patient-vitals-raw")

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")

def generate_synthetic_vitals(patient_count=5, interval_sec=1.0):
    """Generate realistic vital sign streams."""
    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS})
    patients = [f"PATIENT-{i:03d}" for i in range(1, patient_count + 1)]
    sensors = ["HEART_RATE", "SPO2", "BLOOD_PRESSURE_SYS", "TEMPERATURE"]

    print(f"Starting synthetic data generator for {patient_count} patients...")

    try:
        while True:
            for patient_id in patients:
                for sensor in sensors:
                    # Generate base value with some noise
                    if sensor == "HEART_RATE":
                        value = random.normalvariate(75, 5)
                    elif sensor == "SPO2":
                        value = random.normalvariate(98, 1)
                    elif sensor == "BLOOD_PRESSURE_SYS":
                        value = random.normalvariate(120, 10)
                    else: # TEMPERATURE
                        value = random.normalvariate(37, 0.5)

                    data = {
                        "time": datetime.now(timezone.utc).isoformat(),
                        "patient_id": patient_id,
                        "sensor_type": sensor,
                        "value": round(value, 2)
                    }

                    producer.produce(
                        KAFKA_TOPIC_RAW,
                        key=patient_id,
                        value=json.dumps(data).encode("utf-8"),
                        callback=delivery_report
                    )
            
            producer.flush()
            time.sleep(interval_sec)
    except KeyboardInterrupt:
        print("Generator stopped.")

if __name__ == "__main__":
    generate_synthetic_vitals()
