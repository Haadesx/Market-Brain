from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Any

class BaseModel(ABC):
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict using the trained model."""
        pass

    @abstractmethod
    def save(self, path: str):
        """Save model artifacts to path."""
        pass

    @abstractmethod
    def load(self, path: str):
        """Load model artifacts from path."""
        pass
