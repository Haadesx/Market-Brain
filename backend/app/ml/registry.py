import mlflow
from mlflow.tracking import MlflowClient

class ModelRegistry:
    def __init__(self):
        self.client = MlflowClient()

    def list_models(self):
        return self.client.search_registered_models()

    def promote_model(self, model_name: str, version: str, stage: str = "Production"):
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )

    def get_production_model(self, model_name: str):
        models = self.client.get_latest_versions(model_name, stages=["Production"])
        if not models:
            return None
        return models[0]
