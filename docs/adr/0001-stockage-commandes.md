# ADR-0001 — Où stocker les commandes (Historique d'Inférence)

**Status :** Proposé
**Date :** 06/10/2026

## Contexte
Notre API de Machine Learning évalue des commandes en temps réel pour prédire leur éligibilité à la livraison express (`express_eligible`). Ces commandes contiennent diverses caractéristiques (`distance_km`, `weather`, `customer_type`, etc.).
Nous devons stocker l'intégralité des commandes reçues ainsi que la décision du modèle afin de :
1. Assurer la traçabilité et l'auditabilité des décisions.
2. Monitorer la dérive des données (data drift).
3. Alimenter la collecte de données (`OrderDataProvider`) pour les futurs réentraînements du modèle Scikit-Learn.
Les caractéristiques (features) de ces commandes sont amenées à évoluer fréquemment lors des prochaines itérations ML (ajout de nouvelles variables).

## Options considérées

* **Option A. Base de données relationnelle (ex: PostgreSQL)**
  * **Avantages :** Standard de l'industrie, requêtes SQL natives et intégrité des données.
  * **Inconvénients :** Schéma tabulaire rigide. L'ajout fréquent de nouvelles features ML obligerait à faire des migrations de schéma régulières.
* **Option B. Base de données NoSQL Orientée Document (ex: MongoDB)**
  * **Avantages :** Flexibilité du schéma. Permet de stocker facilement le dictionnaire JSON de la commande d'entrée, même si des clés sont ajoutées ou supprimées d'une version du modèle à l'autre. Excellente scalabilité en écriture.
  * **Inconvénients :** Moins adapté si l'on devait faire des jointures complexes avec d'autres entités métier, mais ce n'est pas le cas pour un log d'inférence.
* **Option C. Data Lake / Object Storage en mode Batch (ex: AWS S3 + Parquet)**
  * **Avantages :** Format optimisé pour la lecture analytique et le réentraînement ML avec Pandas.
  * **Inconvénients :** Ne supporte pas l'écriture unitaire en temps réel lors de chaque prédiction, nécessiterait une architecture plus complexe avec un buffer intermédiaire (ex: Kafka + Spark Streaming).

## Décision
**Option B (Base de données NoSQL Orientée Document)**

*Justification :* Dans le contexte d'une API d'inférence ML, la flexibilité du schéma est un avantage majeur. Nous pouvons simplement sérialiser l'objet `valid_order` reçu et la réponse de notre `OrderPredictor` en un seul document. Cela réduit la friction entre l'équipe Data Science (qui ajoute des features) et l'équipe d'ingénierie (qui gère la BDD).

## Conséquence
* **Infrastructure :** Nous devons provisionner une base NoSQL document (MongoDB ou équivalent).
* **Code :** La méthode `generate_data()` de la classe `OrderDataProvider` (ainsi que la gestion des données) devra être capable de lire cette collection de documents et de l'aplatir (flatten) pour générer le `pd.DataFrame` nécessaire au `ScikitModelTrainer`.
