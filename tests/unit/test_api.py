import pytest
from unittest.mock import patch
from src.api.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@patch("src.api.routes.fetch_patients")
def test_get_patients(mock_fetch, client):
    """Test /api/patients endpoint."""
    mock_fetch.return_value = ["PATIENT-001", "PATIENT-002"]
    
    response = client.get("/api/patients")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["data"] == ["PATIENT-001", "PATIENT-002"]

@patch("src.api.routes.fetch_vitals")
def test_get_patient_vitals(mock_fetch, client):
    """Test /api/vitals/<patient_id> endpoint."""
    mock_fetch.return_value = [
        {"time": "2026-03-16T10:00:00Z", "sensor_type": "HEART_RATE", "value": 75.0, "anomaly_score": 0.01}
    ]
    
    response = client.get("/api/vitals/PATIENT-001")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["patient_id"] == "PATIENT-001"
    assert len(data["data"]) == 1
    assert data["data"][0]["sensor_type"] == "HEART_RATE"

@patch("src.api.routes.fetch_anomalies")
def test_get_anomalies(mock_fetch, client):
    """Test /api/anomalies endpoint."""
    mock_fetch.return_value = [
        {"time": "2026-03-16T10:05:00Z", "patient_id": "P-001", "severity": "HIGH", "score": 0.9}
    ]
    
    response = client.get("/api/anomalies")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "success"
    assert len(data["data"]) == 1
    assert data["data"][0]["severity"] == "HIGH"

def test_health_check(client):
    """Test /api/health endpoint."""
    response = client.get("/api/health")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["status"] == "healthy"
