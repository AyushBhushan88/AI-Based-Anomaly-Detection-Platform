import pytest
from psycopg import connect

def test_db_connection_ssl(db_url):
    """Confirm SSL is required and active."""
    assert "sslmode=require" in db_url
    with connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SHOW ssl;")
            ssl_status = cur.fetchone()[0]
            assert ssl_status == "on", "SSL is not enabled on the database connection"

def test_timescaledb_extension(db_connection):
    """Verify TimescaleDB extension is active."""
    with db_connection.cursor() as cur:
        cur.execute("SELECT extname FROM pg_extension WHERE extname = 'timescaledb';")
        extension = cur.fetchone()
        assert extension is not None, "TimescaleDB extension is not installed"
        assert extension[0] == "timescaledb"
