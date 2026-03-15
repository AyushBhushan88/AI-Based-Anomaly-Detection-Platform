import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

class Preprocessor:
    """Handles normalization, noise filtering, and data cleaning for vital sign data."""
    
    # Clinical-grade plausible ranges for clipping (to handle sensor malfunctions)
    SENSOR_RANGES = {
        "HEART_RATE": (30, 220),
        "SPO2": (50, 100),
        "BLOOD_PRESSURE_SYS": (60, 250),
        "TEMPERATURE": (30, 45)
    }

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.is_fitted = False
        self.sensors = ["HEART_RATE", "SPO2", "BLOOD_PRESSURE_SYS", "TEMPERATURE"]
        
    def fit(self, data: pd.DataFrame):
        """Fit the scaler on normal training data."""
        # Ensure we only fit on columns we expect
        clean_data = self.clip_values(data[self.sensors])
        self.scaler.fit(clean_data)
        self.is_fitted = True
        
    def transform(self, data: pd.DataFrame) -> np.ndarray:
        """Normalize the data."""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform.")
        # Apply cleaning before transformation
        clean_data = self.clip_values(data[self.sensors])
        return self.scaler.transform(clean_data)
    
    def clip_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clip extreme sensor readings to plausible physiological ranges."""
        clipped_df = df.copy()
        for sensor, (min_val, max_val) in self.SENSOR_RANGES.items():
            if sensor in clipped_df.columns:
                clipped_df[sensor] = clipped_df[sensor].clip(lower=min_val, upper=max_val)
        return clipped_df

    def impute_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fill missing values using linear interpolation or default normals."""
        imputed_df = df.copy()
        # 1. Forward fill (use last known value)
        imputed_df = imputed_df.ffill()
        # 2. Fill remaining with median (if first readings are missing)
        defaults = {
            "HEART_RATE": 75,
            "SPO2": 98,
            "BLOOD_PRESSURE_SYS": 120,
            "TEMPERATURE": 37
        }
        for sensor, default in defaults.items():
            if sensor in imputed_df.columns:
                imputed_df[sensor] = imputed_df[sensor].fillna(default)
        return imputed_df

    def apply_noise_filter(self, df: pd.DataFrame, window=3) -> pd.DataFrame:
        """Apply a simple moving average filter to smooth sensor noise."""
        filtered_df = df.copy()
        for sensor in self.sensors:
            filtered_df[sensor] = df[sensor].rolling(window=window, min_periods=1).mean()
        return filtered_df

    def save(self, path: str):
        """Save the fitted scaler artifact."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.scaler, path)
        print(f"Preprocessor scaler saved to {path}")

    def load(self, path: str):
        """Load a fitted scaler artifact."""
        self.scaler = joblib.load(path)
        self.is_fitted = True
        print(f"Preprocessor scaler loaded from {path}")
