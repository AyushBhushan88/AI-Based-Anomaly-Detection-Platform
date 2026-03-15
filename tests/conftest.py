import os
import pytest
from psycopg import connect
from confluent_kafka.admin import AdminClient
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def db_url():
    return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/vitals")

@pytest.fixture(scope="session")
def kafka_bootstrap_servers():
    return os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

@pytest.fixture(scope="session")
def db_connection(db_url):
    with connect(db_url) as conn:
        yield conn

@pytest.fixture(scope="session")
def kafka_admin(kafka_bootstrap_servers):
    return AdminClient({"bootstrap.servers": kafka_bootstrap_servers})
