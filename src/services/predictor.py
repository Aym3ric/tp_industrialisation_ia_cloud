import pandas as pd
import numpy as np
from datetime import datetime
from src.abstractions.model import IOrderPredictor, IModelLoader
from src.abstractions.config import IConfig

class OrderPredictor(IOrderPredictor):
    def __init__(self, model_loader: IModelLoader, config: IConfig):
        """
        Initialise le prédicteur.
        """
        self.model = model_loader.load_model()
        self.feature_columns = model_loader.feature_columns
        self.model_version = config.model_version

    def predict_batch(self, input_df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        """
        Réalise une prédiction batch sur plusieurs commandes.
        """
        missing_features = set(self.feature_columns) - set(input_df.columns)
        if missing_features:
            raise ValueError(
                f"Variables manquantes dans le batch : {sorted(missing_features)}"
            )

        result = input_df.copy()
        result["eligibility_probability"] = self.model.predict_proba(
            input_df[self.feature_columns]
        )[:, 1]

        result["express_eligible"] = (
            result["eligibility_probability"] >= threshold
        ).astype(int)

        result["decision"] = np.where(
            result["express_eligible"] == 1,
            "oui",
            "non"
        )

        return result

    def predict_single(self, order_data: dict, threshold: float = 0.5) -> dict:
        """
        Effectue une prédiction pour une commande (temps réel).
        """
        missing_features = set(self.feature_columns) - set(order_data.keys())
        if missing_features:
            raise ValueError(
                f"Variables manquantes : {sorted(missing_features)}"
            )

        input_df = pd.DataFrame(
            [{feature: order_data[feature] for feature in self.feature_columns}]
        )

        probability = float(self.model.predict_proba(input_df)[0, 1])
        eligible = probability >= threshold

        return {
            "express_eligible": bool(eligible),
            "decision": "oui" if eligible else "non",
            "probability": round(probability, 4),
            "model_version": self.model_version,
            "prediction_timestamp": datetime.utcnow().isoformat()
        }
