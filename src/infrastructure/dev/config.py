from pathlib import Path
from src.abstractions.config import IConfig

class DevConfig(IConfig):
    @property
    def base_dir(self) -> Path:
        return Path(__file__).parent.parent.parent.parent

    @property
    def artifacts_dir(self) -> Path:
        path = self.base_dir / "artifacts" / "dev"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def model_path(self) -> Path:
        return self.artifacts_dir / "express_delivery_model.joblib"

    @property
    def features_path(self) -> Path:
        return self.artifacts_dir / "features.json"

    @property
    def metrics_path(self) -> Path:
        return self.artifacts_dir / "metrics.json"

    @property
    def dataset_size(self) -> int:
        return 1000  # Smaller dataset for dev

    @property
    def mlflow_experiment_name(self) -> str:
        return "livraison-express-dev"

    @property
    def model_version(self) -> str:
        return "1.0.0-dev"
