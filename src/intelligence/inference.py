import os
import torch
import joblib
import numpy as np
import pandas as pd
from src.intelligence.models import Autoencoder, IsolationForestWrapper
from src.intelligence.preprocessor import Preprocessor

class InferenceEngine:
    """
    Handles real-time anomaly scoring for patient vital signs.
    Aggregates per-sensor messages into full feature vectors before scoring.
    """
    
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.preprocessor = Preprocessor()
        self.ae = Autoencoder(input_dim=4)
        self.if_wrapper = IsolationForestWrapper()
        
        self._load_models()
        
        # Buffer for per-patient sensor data
        self.buffer = {}
        # Buffer for historical feature vectors (rolling window for noise filtering)
        self.history = {}
        self.HISTORY_WINDOW = 5
        
        self.sensors = ["HEART_RATE", "SPO2", "BLOOD_PRESSURE_SYS", "TEMPERATURE"]
        
        # Thresholds (calibrated for anomaly detection)
        # These can be dynamic in a real system.
        self.AE_THRESHOLD = 0.5  # Re-calibrated based on trainer loss
        self.IF_THRESHOLD = 0.2  # Decision function distance (inverted)
        
    def _load_models(self):
        """Load fitted models and scalers from disk."""
        scaler_path = os.path.join(self.models_dir, "scaler.joblib")
        ae_path = os.path.join(self.models_dir, "autoencoder.pt")
        if_path = os.path.join(self.models_dir, "isolation_forest.joblib")
        
        if os.path.exists(scaler_path):
            self.preprocessor.load(scaler_path)
        if os.path.exists(ae_path):
            self.ae.load_state_dict(torch.load(ae_path))
            self.ae.eval()
        if os.path.exists(if_path):
            self.if_wrapper.load(if_path)
            
    def process_sensor_data(self, patient_id, sensor_type, value):
        """
        Incorporate a new sensor reading. 
        Returns (score, severity) if a full feature vector is formed, else None.
        """
        if patient_id not in self.buffer:
            self.buffer[patient_id] = {}
            
        self.buffer[patient_id][sensor_type] = value
        
        # Check if we have all sensors
        if all(s in self.buffer[patient_id] for s in self.sensors):
            # Create feature vector
            vitals = [self.buffer[patient_id][s] for s in self.sensors]
            
            # Reset buffer for this patient
            self.buffer[patient_id] = {}
            
            # Add to history for noise filtering
            if patient_id not in self.history:
                self.history[patient_id] = []
            
            self.history[patient_id].append(vitals)
            
            # Keep only the last N samples
            if len(self.history[patient_id]) > self.HISTORY_WINDOW:
                self.history[patient_id].pop(0)
                
            # Apply noise filter if we have enough samples
            if len(self.history[patient_id]) >= 3:
                # Convert history to DataFrame for filtering
                df_history = pd.DataFrame(self.history[patient_id], columns=self.sensors)
                # Filter (moving average)
                df_filtered = self.preprocessor.apply_noise_filter(df_history, window=3)
                # Take the latest filtered sample
                latest_vitals = df_filtered.iloc[-1].tolist()
                return self.score(latest_vitals)
            else:
                # Not enough history yet, score raw current vitals
                return self.score(vitals)
        
        return None

    def score(self, vitals_list):
        """
        Compute anomaly score and severity.
        vitals_list: [HEART_RATE, SPO2, BLOOD_PRESSURE_SYS, TEMPERATURE]
        """
        # Convert to DataFrame for preprocessor
        df = pd.DataFrame([vitals_list], columns=self.sensors)
        X = self.preprocessor.transform(df)
        X_tensor = torch.FloatTensor(X)
        
        # 1. Autoencoder Score
        ae_err = self.ae.get_reconstruction_error(X_tensor)[0]
        
        # 2. Isolation Forest Score
        if_score = self.if_wrapper.get_anomaly_score(X)[0]
        
        # 3. Ensemble (weighted average or max)
        # Normalizing scores to [0, 1] for unified display.
        # AE error is raw MSE, IF score is -signed_proximity.
        combined_score = (ae_err + if_score) / 2.0
        
        severity = self._get_severity(ae_err, if_score)
        
        return float(combined_score), severity

    def _get_severity(self, ae_err, if_score):
        """Classify severity based on model outputs."""
        # High severity if both models strongly agree or one is extreme
        if ae_err > self.AE_THRESHOLD * 2 or if_score > self.IF_THRESHOLD * 2:
            return "HIGH"
        elif ae_err > self.AE_THRESHOLD or if_score > self.IF_THRESHOLD:
            return "MEDIUM"
        else:
            return "LOW"
