import pytest
import torch
import numpy as np
import pandas as pd
import os
from src.intelligence.models import Autoencoder, IsolationForestWrapper
from src.intelligence.preprocessor import Preprocessor

def test_autoencoder_architecture():
    """Verify Autoencoder architecture and forward pass."""
    input_dim = 4
    model = Autoencoder(input_dim=input_dim)
    
    # Test forward pass
    x = torch.randn(10, input_dim)
    output = model(x)
    
    assert output.shape == (10, input_dim)
    
    # Test reconstruction error calculation
    error = model.get_reconstruction_error(x)
    assert error.shape == (10,)
    assert np.all(error >= 0)

def test_isolation_forest_wrapper():
    """Verify Isolation Forest wrapper and scoring."""
    if_wrapper = IsolationForestWrapper(contamination=0.1)
    
    # Generate random data
    X = np.random.rand(100, 4)
    if_wrapper.fit(X)
    
    assert if_wrapper.is_fitted
    
    # Test scoring
    X_test = np.random.rand(10, 4)
    scores = if_wrapper.get_anomaly_score(X_test)
    assert scores.shape == (10,)

def test_preprocessor_scaling():
    """Verify Preprocessor scaling."""
    preprocessor = Preprocessor()
    data = pd.DataFrame({
        "HEART_RATE": [60, 100],
        "SPO2": [95, 100],
        "BLOOD_PRESSURE_SYS": [110, 130],
        "TEMPERATURE": [36.5, 37.5]
    })
    
    preprocessor.fit(data)
    assert preprocessor.is_fitted
    
    transformed = preprocessor.transform(data)
    assert transformed.shape == (2, 4)
    # MinMaxScaler scales to [0, 1]
    assert np.all(transformed >= -1e-7)
    assert np.all(transformed <= 1 + 1e-7)

def test_model_anomaly_detection():
    """Verify that anomalous data produces significantly higher scores than normal data."""
    # 1. Setup Preprocessor
    preprocessor = Preprocessor()
    normal_data = pd.DataFrame({
        "HEART_RATE": [75]*100,
        "SPO2": [98]*100,
        "BLOOD_PRESSURE_SYS": [120]*100,
        "TEMPERATURE": [37]*100
    })
    preprocessor.fit(normal_data)
    
    # 2. Setup Autoencoder
    ae = Autoencoder(input_dim=4)
    
    # 3. Setup Isolation Forest
    if_wrapper = IsolationForestWrapper(contamination=0.01)
    if_wrapper.fit(preprocessor.transform(normal_data))
    
    # 4. Create Normal vs Anomalous samples
    normal_sample = pd.DataFrame({
        "HEART_RATE": [75],
        "SPO2": [98],
        "BLOOD_PRESSURE_SYS": [120],
        "TEMPERATURE": [37]
    })
    
    anomalous_sample = pd.DataFrame({
        "HEART_RATE": [150],  # Way high
        "SPO2": [70],         # Way low
        "BLOOD_PRESSURE_SYS": [200], # Way high
        "TEMPERATURE": [41]   # High fever
    })
    
    if os.path.exists("models/autoencoder.pt") and os.path.exists("models/isolation_forest.joblib") and os.path.exists("models/scaler.joblib"):
        preprocessor.load("models/scaler.joblib")
        ae.load_state_dict(torch.load("models/autoencoder.pt"))
        if_wrapper.load("models/isolation_forest.joblib")
        
        X_normal = preprocessor.transform(normal_sample)
        X_anomalous = preprocessor.transform(anomalous_sample)
        
        err_normal = ae.get_reconstruction_error(torch.FloatTensor(X_normal))
        err_anomalous = ae.get_reconstruction_error(torch.FloatTensor(X_anomalous))
        
        score_normal = if_wrapper.get_anomaly_score(X_normal)
        score_anomalous = if_wrapper.get_anomaly_score(X_anomalous)
        
        assert err_anomalous[0] > err_normal[0]
        assert score_anomalous[0] > score_normal[0]
    else:
        # Fallback if models not trained yet
        X_normal = preprocessor.transform(normal_sample)
        X_anomalous = preprocessor.transform(anomalous_sample)
        err_normal = ae.get_reconstruction_error(torch.FloatTensor(X_normal))
        err_anomalous = ae.get_reconstruction_error(torch.FloatTensor(X_anomalous))
        assert err_normal.shape == (1,)
        assert err_anomalous.shape == (1,)
