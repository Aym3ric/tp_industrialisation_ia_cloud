from abc import ABC, abstractmethod
import pandas as pd

class IModelTrainer(ABC):
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

class IModelLoader(ABC):
    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def load_features_config(self) -> dict:
        pass

class IOrderPredictor(ABC):
    @abstractmethod
    def predict_batch(self, input_df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        pass

    @abstractmethod
    def predict_single(self, order_data: dict, threshold: float = 0.5) -> dict:
        pass

class IModelEvaluator(ABC):
    @abstractmethod
    def evaluate(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        pass
