import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vitals?sslmode=require")

def get_db_connection():
    """Establish a connection to the TimescaleDB."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def fetch_patients():
    """Retrieve unique patient IDs from the vitals table."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT patient_id FROM vitals ORDER BY patient_id")
            return [row["patient_id"] for row in cur.fetchall()]

def fetch_vitals(patient_id, limit=100):
    """Retrieve recent vitals for a specific patient."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT time, sensor_type, value, anomaly_score 
                FROM vitals 
                WHERE patient_id = %s 
                ORDER BY time DESC 
                LIMIT %s
                """,
                (patient_id, limit)
            )
            return cur.fetchall()

def fetch_anomalies(limit=50):
    """Retrieve recent anomaly events."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT time, patient_id, sensor_type, severity, score, details 
                FROM anomalies 
                ORDER BY time DESC 
                LIMIT %s
                """,
                (limit,)
            )
            return cur.fetchall()
