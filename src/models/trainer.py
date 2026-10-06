import json
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from src.abstractions.model import IModelTrainer, IModelEvaluator
from src.abstractions.config import IConfig

class ScikitModelTrainer(IModelTrainer):
    def __init__(self, config: IConfig):
        self.config = config
        self.numeric_features = [
            "hour", "day_of_week", "weekend", "distance_km",
            "order_value_eur", "weight_kg", "stock_available",
            "preparation_time_min", "carrier_capacity",
        ]
        self.categorical_features = [
            "weather", "delivery_zone", "customer_type",
        ]
        self.feature_columns = self.numeric_features + self.categorical_features

    def _build_pipeline(self):
        numeric_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])

        categorical_transformer = Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])

        preprocessor = ColumnTransformer(transformers=[
            ("numeric", numeric_transformer, self.numeric_features),
            ("categorical", categorical_transformer, self.categorical_features),
        ])

        classifier = LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )

        return Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ])

    def train(self, X: pd.DataFrame, y: pd.Series, evaluator: IModelEvaluator) -> None:
        X = X[self.feature_columns]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )

        model_pipeline = self._build_pipeline()

        mlflow.set_experiment(self.config.mlflow_experiment_name)

        with mlflow.start_run(run_name="logistic-regression-baseline") as run:
            model_pipeline.fit(X_train, y_train)

            # Délégation de l'évaluation
            metrics = evaluator.evaluate(model_pipeline, X_test, y_test)

            mlflow.log_param("model_type", "LogisticRegression")
            mlflow.log_param("random_state", 42)
            mlflow.log_param("feature_count", len(self.feature_columns))

            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)

            try:
                mlflow.sklearn.log_model(model_pipeline, artifact_path="model")
            except Exception as e:
                print(f"MLFlow log_model error (skops_trusted_types issue): {e}")

            # Save artifacts locally
            joblib.dump(model_pipeline, self.config.model_path)
            
            with open(self.config.features_path, "w", encoding="utf-8") as f:
                json.dump({"features": self.feature_columns}, f)

            with open(self.config.metrics_path, "w", encoding="utf-8") as f:
                json.dump(metrics, f)

            print(f"Entraînement terminé. Modèle sauvegardé dans {self.config.artifacts_dir}")
