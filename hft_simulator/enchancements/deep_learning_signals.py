import numpy as np
import pandas as pd
from typing import Tuple, Any
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

class PricePredictorNN(nn.Module):
    """Simple feedforward neural network for price movement prediction."""
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

    def forward(self, x):
        return self.net(x)

def preprocess_data(
    df: pd.DataFrame, 
    feature_cols: list, 
    target_col: str, 
    window_size: int = 20
) -> Tuple[np.ndarray, np.ndarray, Any]:
    """
    Prepares time series data for neural network input.
    Returns: X (samples, window*features), y (samples,), scaler
    """
    scaler = StandardScaler()
    features = scaler.fit_transform(df[feature_cols])
    X, y = [], []
    for i in range(window_size, len(df)):
        X.append(features[i-window_size:i].flatten())
        y.append(df[target_col].iloc[i])
    return np.array(X), np.array(y), scaler

def train_model(
    X: np.ndarray, 
    y: np.ndarray, 
    input_dim: int, 
    epochs: int = 10, 
    lr: float = 1e-3
) -> PricePredictorNN:
    """Train the neural network on historical data."""
    model = PricePredictorNN(input_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    X_tensor = torch.tensor(X, dtype=torch.float32)
    y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        preds = model(X_tensor)
        loss = loss_fn(preds, y_tensor)
        loss.backward()
        optimizer.step()
    return model

def predict_next(
    model: PricePredictorNN, 
    recent_window: np.ndarray
) -> float:
    """Generate a prediction for the next price movement."""
    model.eval()
    with torch.no_grad():
        x = torch.tensor(recent_window.flatten()[None, :], dtype=torch.float32)
        pred = model(x)
        return float(pred.item())

# Example usage:
# df = pd.read_csv("data/sample_ticks.csv")
# feature_cols = ["price", "volume"]
# X, y, scaler = preprocess_data(df, feature_cols, target_col="price", window_size=20)
# model = train_model(X, y, input_dim=X.shape[1], epochs=20)
# recent_window = scaler.transform(df[feature_cols].iloc[-20:].values)
#