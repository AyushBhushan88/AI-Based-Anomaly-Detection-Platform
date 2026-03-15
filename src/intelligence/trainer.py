import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
import random
from src.intelligence.models import Autoencoder, IsolationForestWrapper
from src.intelligence.preprocessor import Preprocessor

def generate_normal_data(samples=1000):
    """Simulate 'normal' vital signs for training."""
    data = []
    for _ in range(samples):
        # Normal ranges
        hr = random.normalvariate(75, 5)        # 60-100 is normal
        spo2 = random.normalvariate(98, 1)      # 95-100 is normal
        bp_sys = random.normalvariate(120, 10)  # 110-130 is normal
        temp = random.normalvariate(37, 0.5)    # 36.5-37.5 is normal
        
        data.append([hr, spo2, bp_sys, temp])
    
    return pd.DataFrame(data, columns=["HEART_RATE", "SPO2", "BLOOD_PRESSURE_SYS", "TEMPERATURE"])

def train():
    """Train the preprocessing and ML models on normal data."""
    print("Generating normal training data...")
    df_train = generate_normal_data(5000)
    
    # 1. Fit and save Preprocessor
    print("Fitting preprocessor...")
    preprocessor = Preprocessor()
    preprocessor.fit(df_train)
    preprocessor.save("models/scaler.joblib")
    
    X_train = preprocessor.transform(df_train)
    X_train_tensor = torch.FloatTensor(X_train)
    
    # 2. Train and save Autoencoder
    print("Training Autoencoder...")
    ae = Autoencoder(input_dim=4)
    optimizer = optim.Adam(ae.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    epochs = 50
    for epoch in range(epochs):
        ae.train()
        optimizer.zero_grad()
        outputs = ae(X_train_tensor)
        loss = criterion(outputs, X_train_tensor)
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}")
            
    torch.save(ae.state_dict(), "models/autoencoder.pt")
    print("Autoencoder saved to models/autoencoder.pt")
    
    # 3. Fit and save Isolation Forest
    print("Fitting Isolation Forest...")
    if_wrapper = IsolationForestWrapper(contamination=0.01)
    if_wrapper.fit(X_train)
    if_wrapper.save("models/isolation_forest.joblib")
    
    print("\nTraining complete.")

if __name__ == "__main__":
    train()
