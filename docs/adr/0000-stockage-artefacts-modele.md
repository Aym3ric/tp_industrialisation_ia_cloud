# ADR-0000 — Où stocker les artéfacts du modèle de Machine Learning

**Status :** Proposé
**Date :** 06/10/2026

## Contexte
L'API doit pouvoir recharger un modèle au démarrage sans réentraîner à chaque redéploiement.

## Options considérées

* **Option A. Répertoire local**
  * **Avantage :** Aucun service à installer
  * **Inconvénient :** Pas de versionnage fiable
* **Option B. Système de fichiers réseau**
  * **Avantage :** Partage simple entre les deux machines
  * **Inconvénient :** Accès concurrents pénibles
* **Option C. Model Registry ou équivalent**
  * **Avantage :** Versionnage natif
  * **Inconvénient :** Service supplémentaire à maintenir

## Décision
Option A car plus simple a mettre en place.
Évolution probable vers l’option C lorsqu'on aura plusieurs version de modèles.

## Conséquence
* Chaque version du modèle doit être identifiée explicitement.
* Le jour où on aura plusieurs version de modèles, cette ADR devra être marquée “Status: Superseded by ADR-000X” + nouvelle décision écrite.
