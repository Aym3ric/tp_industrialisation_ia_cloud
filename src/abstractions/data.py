from abc import ABC, abstractmethod
import pandas as pd

class IDataProvider(ABC):
    @abstractmethod
    def generate_data(self) -> pd.DataFrame:
        pass

class IDataValidator(ABC):
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        pass

class IDataCleaner(ABC):
    @abstractmethod
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
