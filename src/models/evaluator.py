import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report, confusion_matrix
from src.abstractions.model import IModelEvaluator
from src.abstractions.config import IConfig

class ScikitModelEvaluator(IModelEvaluator):
    def __init__(self, config: IConfig):
        self.config = config

    def evaluate(self, model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """
        Évalue le modèle, affiche les résultats et retourne les métriques.
        """
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1_score": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_proba),
        }

        print("Métriques du modèle :")
        for metric_name, metric_value in metrics.items():
            print(f"{metric_name:>10} : {metric_value:.4f}")

        print("\n" + classification_report(
            y_test,
            y_pred,
            target_names=["Non éligible", "Éligible"],
            zero_division=0
        ))

        # Génération de la matrice de confusion
        conf_matrix = confusion_matrix(y_test, y_pred)

        plt.figure(figsize=(6, 5))
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=["Non éligible", "Éligible"],
            yticklabels=["Non éligible", "Éligible"]
        )

        plt.title("Matrice de confusion")
        plt.xlabel("Prédiction")
        plt.ylabel("Valeur réelle")
        
        # Sauvegarde de la figure au lieu de l'afficher pour ne pas bloquer le script
        plot_path = self.config.artifacts_dir / "confusion_matrix.png"
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()
        print(f"Matrice de confusion sauvegardée dans : {plot_path}")

        return metrics
