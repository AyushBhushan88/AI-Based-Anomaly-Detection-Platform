import pytest
from psycopg import connect

def test_vitals_table_exists(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'vitals'
            );
        """)
        assert cur.fetchone()[0] is True

def test_anomalies_table_exists(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'anomalies'
            );
        """)
        assert cur.fetchone()[0] is True

def test_alerts_table_exists(db_connection):
    with db_connection.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alerts'
            );
        """)
        assert cur.fetchone()[0] is True
