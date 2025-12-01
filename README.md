# Exercice 2 – Pipeline ML complet (DVC + RandomForest)

Ce projet correspond à la correction de l’Exercice 2 : création d’un pipeline ML complet avec DVC.

## 1. Prérequis

- Python 3.10+
- `pip`
- `git`
- `dvc`

## 2. Installation

```bash
python -m venv venv
source venv/bin/activate  # sous Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Initialisation du projet

```bash
git init
dvc init
```

## 4. Préparation des données

1. Générer le dataset Iris brut :
   ```bash
   python scripts/download_iris.py
   ```

2. Prétraitement et création de `data/iris_preprocessed.csv` :
   ```bash
   dvc repro prepare
   ```
   ou directement :
   ```bash
   python scripts/preprocess.py
   ```

## 5. Exécution du pipeline ML complet

```bash
dvc repro
```

Cela exécute les stages définis dans `dvc.yaml` :
- `prepare` : prétraitement du dataset,
- `train` : entraînement du modèle RandomForest,
- `evaluate` : évaluation globale et sauvegarde des métriques.

Les sorties importantes sont :
- `models/random_forest.pkl` : modèle entraîné,
- `metrics/train_metrics.json` : métriques d'entraînement,
- `metrics/eval_metrics.json` : métriques d'évaluation globale.
