import torch
import torch.nn as nn
from sklearn.ensemble import IsolationForest
import joblib
import os

class Autoencoder(nn.Module):
    """
    A deep autoencoder for medical vital sign anomaly detection.
    High reconstruction error indicates a deviation from normal patterns.
    """
    def __init__(self, input_dim=4):
        super(Autoencoder, self).__init__()
        
        # Encoder: 4 -> 8 -> 4 -> 2
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 2)
        )
        
        # Decoder: 2 -> 4 -> 8 -> 4
        self.decoder = nn.Sequential(
            nn.Linear(2, 4),
            nn.ReLU(),
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

    def get_reconstruction_error(self, x):
        """Compute the Mean Squared Error of the reconstruction."""
        self.eval()
        with torch.no_grad():
            reconstructed = self.forward(x)
            mse = nn.MSELoss(reduction='none')(reconstructed, x)
            return mse.mean(dim=1).numpy()

class IsolationForestWrapper:
    """Wrapper for Scikit-learn's Isolation Forest to provide a unified interface."""
    
    def __init__(self, contamination=0.01):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False

    def fit(self, X):
        self.model.fit(X)
        self.is_fitted = True

    def get_anomaly_score(self, X):
        """
        Compute anomaly score. 
        Original score: Lower is more anomalous.
        Inverted score: Higher is more anomalous.
        """
        if not self.is_fitted:
            raise ValueError("Isolation Forest must be fitted before scoring.")
        # decision_function returns signed proximity: lower means more anomalous
        scores = self.model.decision_function(X)
        return -scores # Invert so higher is more anomalous

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.model, path)
        print(f"Isolation Forest saved to {path}")

    def load(self, path: str):
        self.model = joblib.load(path)
        self.is_fitted = True
        print(f"Isolation Forest loaded from {path}")
