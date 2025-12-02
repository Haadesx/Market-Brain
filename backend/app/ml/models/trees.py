import pandas as pd
import numpy as np
import xgboost as xgb
from app.ml.base import BaseModel

class XGBoostModel(BaseModel):
    def __init__(self, params: dict = None):
        self.params = params or {
            'objective': 'reg:squarederror',
            'n_estimators': 100,
            'max_depth': 3,
            'learning_rate': 0.1
        }
        self.model = xgb.XGBRegressor(**self.params)

    def train(self, X: pd.DataFrame, y: pd.Series, **kwargs):
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

    def save(self, path: str):
        self.model.save_model(path)

    def load(self, path: str):
        self.model.load_model(path)
