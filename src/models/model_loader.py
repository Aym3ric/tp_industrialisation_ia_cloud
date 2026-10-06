import json
import joblib
from src.abstractions.model import IModelLoader
from src.abstractions.config import IConfig

class ScikitModelLoader(IModelLoader):
    def __init__(self, config: IConfig):
        """
        Initialise le chargeur avec la configuration.
        """
        self.config = config
        self._model = None
        self._features_config = None

    def load_model(self):
        """
        Charge le modèle scikit-learn (pipeline) depuis le fichier joblib.
        """
        if self._model is None:
            self._model = joblib.load(self.config.model_path)
        return self._model

    def load_features_config(self):
        """
        Charge la configuration des features depuis le fichier json.
        """
        if self._features_config is None:
            with open(self.config.features_path, "r", encoding="utf-8") as file:
                self._features_config = json.load(file)
        return self._features_config

    @property
    def feature_columns(self):
        """
        Retourne la liste des colonnes nécessaires pour la prédiction.
        """
        config = self.load_features_config()
        return config.get("features", [])
