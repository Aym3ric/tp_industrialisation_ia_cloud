import os
import sys

from src.infrastructure.dev.config import DevConfig
from src.infrastructure.test.config import TestConfig
from src.infrastructure.prod.config import ProdConfig

from src.data.provider import OrderDataProvider
from src.data.validator import OrderDataValidator
from src.data.cleaner import OrderDataCleaner
from src.models.trainer import ScikitModelTrainer
from src.models.model_loader import ScikitModelLoader
from src.models.evaluator import ScikitModelEvaluator
from src.services.predictor import OrderPredictor

def get_config(env: str):
    if env == "prod":
        return ProdConfig()
    elif env == "test":
        return TestConfig()
    else:
        return DevConfig()

def run_prediction_tests(predictor):
    valid_order = {
        "hour": 10,
        "day_of_week": 1,
        "weekend": 0,
        "distance_km": 2,
        "order_value_eur": 50,
        "weight_kg": 1,
        "stock_available": 1,
        "preparation_time_min": 10,
        "carrier_capacity": 0.9,
        "weather": "normal",
        "delivery_zone": "centre",
        "customer_type": "premium",
    }

    print("\n--- Test d'une commande valide ---")
    result = predictor.predict_single(valid_order)
    print(f"Résultat : {result}")

    assert result["decision"] in {"oui", "non"}
    assert isinstance(result["express_eligible"], bool)
    assert 0 <= result["probability"] <= 1
    assert "model_version" in result

    print("\n--- Test d'une commande invalide ---")
    invalid_order = valid_order.copy()
    del invalid_order["distance_km"]

    try:
        predictor.predict_single(invalid_order)
        raise AssertionError("Une erreur de variable manquante aurait dû se produire.")
    except ValueError as e:
        print(f"Erreur interceptée avec succès : {e}")

    print("\nTous les tests de prédiction sont passés.")

def main():
    env = os.getenv("APP_ENV", "dev").lower()
    print(f"Lancement de l'orchestrateur dans l'environnement : {env.upper()}")

    # 1. Configuration
    config = get_config(env)
    
    # 2. Données (Génération)
    print("\n--- 1. Collecte des données ---")
    provider = OrderDataProvider(config)
    df_raw = provider.generate_data()
    print(f"{len(df_raw)} commandes générées.")

    # 3. Données (Validation & Nettoyage)
    print("\n--- 2. Qualité et Nettoyage ---")
    validator = OrderDataValidator()
    try:
        validator.validate(df_raw)
        print("Les données générées sont valides.")
    except ValueError as e:
        print(f"Validation échouée : {e}")
        print("Nettoyage des données...")
    
    cleaner = OrderDataCleaner()
    df_clean = cleaner.clean(df_raw)
    print(f"Données nettoyées : {len(df_clean)} commandes restantes.")
    
    validator.validate(df_clean)
    print("Contrôle qualité OK après nettoyage.")

    # 4. Modèle (Entraînement et Évaluation)
    print("\n--- 3. Entraînement et Évaluation du modèle ---")
    X = df_clean
    y = df_clean["express_eligible"]
    
    trainer = ScikitModelTrainer(config)
    evaluator = ScikitModelEvaluator(config)
    trainer.train(X, y, evaluator)

    # 5. Services (Prédiction)
    print("\n--- 4. Chargement et Prédiction ---")
    loader = ScikitModelLoader(config)
    predictor = OrderPredictor(loader, config)
    
    run_prediction_tests(predictor)

if __name__ == "__main__":
    main()
