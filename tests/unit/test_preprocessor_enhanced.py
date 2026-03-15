import pytest
import pandas as pd
import numpy as np
from src.intelligence.preprocessor import Preprocessor

def test_clipping():
    """Verify that extreme values are clipped."""
    preprocessor = Preprocessor()
    data = pd.DataFrame({
        "HEART_RATE": [20, 300],
        "SPO2": [40, 110],
        "BLOOD_PRESSURE_SYS": [50, 300],
        "TEMPERATURE": [25, 50]
    })
    
    clipped = preprocessor.clip_values(data)
    
    # Heart rate: 30-220
    assert clipped["HEART_RATE"].iloc[0] == 30
    assert clipped["HEART_RATE"].iloc[1] == 220
    # SPO2: 50-100
    assert clipped["SPO2"].iloc[0] == 50
    assert clipped["SPO2"].iloc[1] == 100

def test_imputation():
    """Verify that missing values are imputed."""
    preprocessor = Preprocessor()
    data = pd.DataFrame({
        "HEART_RATE": [70, None, 80],
        "SPO2": [None, 98, 97],
        "BLOOD_PRESSURE_SYS": [120, 125, None],
        "TEMPERATURE": [37.0, 37.1, 37.2]
    })
    
    imputed = preprocessor.impute_missing(data)
    
    assert not imputed.isnull().values.any()
    # HEART_RATE at index 1 should be ffilled from index 0
    assert imputed["HEART_RATE"].iloc[1] == 70
    # SPO2 at index 0 should be filled with default 98
    assert imputed["SPO2"].iloc[0] == 98
    # BLOOD_PRESSURE_SYS at index 2 should be ffilled from index 1
    assert imputed["BLOOD_PRESSURE_SYS"].iloc[2] == 125

def test_noise_filtering():
    """Verify moving average filter."""
    preprocessor = Preprocessor()
    data = pd.DataFrame({
        "HEART_RATE": [100, 110, 120],
        "SPO2": [98, 98, 98],
        "BLOOD_PRESSURE_SYS": [120, 120, 120],
        "TEMPERATURE": [37, 37, 37]
    })
    
    filtered = preprocessor.apply_noise_filter(data, window=3)
    
    # Second value should be (100+110)/2 = 105
    assert filtered["HEART_RATE"].iloc[1] == 105
    # Third value should be (100+110+120)/3 = 110
    assert filtered["HEART_RATE"].iloc[2] == 110
