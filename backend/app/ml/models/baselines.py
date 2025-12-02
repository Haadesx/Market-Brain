import pandas as pd
import numpy as np
import pickle
import os
from app.ml.base import BaseModel

class NaiveModel(BaseModel):
    """Predicts the last observed value (random walk hypothesis)."""
    
    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        # No training needed
        pass

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        # Assuming X has a 'close' column which is the last known price
        # If predicting returns, naive might predict 0.
        # Let's assume we are predicting returns, so naive prediction is 0 (martingale)
        # Or if predicting price, it's the last price.
        # For this system, let's assume we predict next period return.
        return np.zeros(len(X))

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump("naive", f)

    def load(self, path: str):
        pass

class MovingAverageModel(BaseModel):
    """Predicts using a simple moving average of recent returns."""
    
    def __init__(self, window: int = 5):
        self.window = window
        self.mean_return = 0.0

    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        # In a real scenario, we might just learn the global mean
        self.mean_return = y.mean()

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        # Return the global mean return
        return np.full(len(X), self.mean_return)

    def save(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self.mean_return, f)

    def load(self, path: str):
        with open(path, 'rb') as f:
            self.mean_return = pickle.load(f)
