from abc import ABC, abstractmethod
from pathlib import Path

class IConfig(ABC):
    @property
    @abstractmethod
    def base_dir(self) -> Path:
        pass

    @property
    @abstractmethod
    def artifacts_dir(self) -> Path:
        pass

    @property
    @abstractmethod
    def model_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def features_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def metrics_path(self) -> Path:
        pass

    @property
    @abstractmethod
    def dataset_size(self) -> int:
        pass

    @property
    @abstractmethod
    def mlflow_experiment_name(self) -> str:
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        pass
