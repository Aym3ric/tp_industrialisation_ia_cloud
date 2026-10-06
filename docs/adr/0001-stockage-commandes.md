# ADR-0001 — Où stocker les commandes (Historique d'Inférence)

**Status :** Proposé
**Date :** 06/10/2026

## Contexte
L'API de Machine Learning évalue des commandes en temps réel pour prédire leur éligibilité à la livraison express (`express_eligible`). Ces commandes contiennent diverses caractéristiques (`distance_km`, `weather`, `customer_type`, etc.).
Nous devons stocker l'intégralité des commandes reçues ainsi que la décision du modèle.

## Options considérées

* **Option A. Base de données relationnelle (ex: PostgreSQL)**
  * **Avantages :** Standard de l'industrie, requêtes SQL natives et intégrité des données.
  * **Inconvénients :** Schéma tabulaire rigide. L'ajout fréquent de nouvelles features ML obligerait à faire des migrations de schéma régulières.
* **Option B. Base de données NoSQL Orientée Document (ex: MongoDB)**
  * **Avantages :** Flexibilité du schéma. Permet de stocker facilement le dictionnaire JSON de la commande d'entrée, même si des clés sont ajoutées ou supprimées d'une version du modèle à l'autre. Excellente scalabilité en écriture.
  * **Inconvénients :** Moins adapté pour des jointures complexes.
* **Option C. Temps réel (ex: Apache Kafka)**
  * **Avantages :** Conçu pour absorber d'importants volumes de données en temps réel. Permet de découpler la réception des commandes de l'inférence (traitement asynchrone) et de brancher facilement d'autres consommateurs sur le flux (ex: pipeline de réentraînement, monitoring).
  * **Inconvénients :** Complexité de mise en œuvre plus élevée (changement d'architecture vers du streaming). Ajoute une brique d'infrastructure lourde à configurer et maintenir.

## Décision
**Option B (Base de données NoSQL Orientée Document)**

*Justification :* Dans le contexte d'une API d'inférence ML, la flexibilité du schéma est un avantage majeur. Nous pouvons simplement sérialiser l'objet reçu et la réponse en un seul document.

## Conséquence
* **Infrastructure :** Nous devons avoir une base NoSQL document (MongoDB ou équivalent).
