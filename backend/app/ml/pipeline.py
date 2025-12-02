import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from app.ml.models.trees import XGBoostModel
from app.ml.models.baselines import NaiveModel
import os

class TrainingPipeline:
    def __init__(self, experiment_name="market_prediction"):
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
        mlflow.set_experiment(experiment_name)

    def run(self, df: pd.DataFrame, target_col: str, model_type: str = "xgboost"):
        """
        Run full training pipeline: Preprocess -> Train -> Evaluate -> Log
        """
        with mlflow.start_run():
            # 1. Prepare Data
            # Assume df has features + target
            X = df.drop(columns=[target_col, "time", "symbol"], errors="ignore")
            y = df[target_col]
            
            # Simple time-based split (no shuffle for time series)
            train_size = int(len(df) * 0.8)
            X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
            y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
            
            # 2. Select Model
            if model_type == "xgboost":
                model = XGBoostModel()
            elif model_type == "naive":
                model = NaiveModel()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
            
            # 3. Train
            mlflow.log_param("model_type", model_type)
            model.train(X_train, y_train)
            
            # 4. Evaluate
            preds = model.predict(X_test)
            rmse = mean_squared_error(y_test, preds, squared=False)
            mae = mean_absolute_error(y_test, preds)
            
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            
            # 5. Save Model
            # MLflow has native support for sklearn/xgboost, but we wrapped them.
            # We can log the wrapper using pickle or custom flavor.
            # For simplicity, let's just log params and metrics for now.
            # In production, we'd use mlflow.pyfunc.log_model(python_model=model)
            
            print(f"Run complete. RMSE: {rmse}")
            return rmse
