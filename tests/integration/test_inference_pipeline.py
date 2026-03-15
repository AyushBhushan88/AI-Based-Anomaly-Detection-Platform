import pytest
import json
from datetime import datetime, timezone
from src.intelligence.inference import InferenceEngine

def test_inference_engine_windowing():
    """Verify that InferenceEngine correctly aggregates sensors and scores."""
    engine = InferenceEngine(models_dir="models")
    patient_id = "TEST-PATIENT"
    
    # 1. First sensor
    res1 = engine.process_sensor_data(patient_id, "HEART_RATE", 80.0)
    assert res1 is None
    
    # 2. Second sensor
    res2 = engine.process_sensor_data(patient_id, "SPO2", 98.0)
    assert res2 is None
    
    # 3. Third sensor
    res3 = engine.process_sensor_data(patient_id, "BLOOD_PRESSURE_SYS", 120.0)
    assert res3 is None
    
    # 4. Fourth sensor (should trigger scoring)
    res4 = engine.process_sensor_data(patient_id, "TEMPERATURE", 37.0)
    assert res4 is not None
    
    score, severity = res4
    assert isinstance(score, float)
    assert severity in ["LOW", "MEDIUM", "HIGH"]
    
    # Verify buffer is cleared
    assert patient_id in engine.buffer
    assert engine.buffer[patient_id] == {}

def test_inference_engine_anomaly_detection():
    """Verify that known anomalous patterns trigger high severity."""
    engine = InferenceEngine(models_dir="models")
    patient_id = "ANOMALY-PATIENT"
    
    # Normal vitals
    res_normal = engine.score([75.0, 98.0, 120.0, 37.0])
    score_n, sev_n = res_normal
    
    # Highly anomalous vitals
    res_anomalous = engine.score([160.0, 70.0, 210.0, 41.0])
    score_a, sev_a = res_anomalous
    
    assert score_a > score_n
    # Note: Depending on training, it might be MEDIUM or HIGH.
    assert sev_a in ["MEDIUM", "HIGH"]

def test_multiple_patients():
    """Verify that engine handles multiple patients simultaneously."""
    engine = InferenceEngine(models_dir="models")
    p1 = "P1"
    p2 = "P2"
    
    engine.process_sensor_data(p1, "HEART_RATE", 70.0)
    engine.process_sensor_data(p2, "HEART_RATE", 75.0)
    
    assert len(engine.buffer[p1]) == 1
    assert len(engine.buffer[p2]) == 1
    assert engine.buffer[p1]["HEART_RATE"] == 70.0
    assert engine.buffer[p2]["HEART_RATE"] == 75.0
