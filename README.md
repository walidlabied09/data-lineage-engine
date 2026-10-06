# 🔄 Pipeline ETL & Machine Learning Orchestré (Modern Data Stack)

Plateforme automatisée de bout en bout conçue pour collecter, transformer, valider et exploiter des données transactionnelles (données de ventes), allant de l'ingestion brute jusqu'à la modélisation prédictive (séries temporelles) et à la restitution décisionnelle.

---

## 🏗️ Architecture Globale du Pipeline

Le pipeline est entièrement orchestré par **Dagster** et s'articule autour d'une base **PostgreSQL** :

```text
 ┌──────────────┐
 │ Dataset CSV  │ (Données de ventes)
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │   Airbyte    │ ─── Écrit les données brutes
 └──────┬───────┘
        │
        ▼
 ┌──────────────┐
 │  PostgreSQL  │ ◄─── Stockage central (Raw & Transformed)
 └──┬─────────┬─┘
    │         │
    │ Lit les │ Écrit les données
    │ brutes  │ transformées
    ▼         │
 ┌──────────────┐
 │     dbt      │ ─── Modélisation : raw ➔ stg_sales_data ➔ fct_sales
 └──────┬───────┘
        │
        ▼
 ┌──────────────────────┐
 │  Great Expectations  │ ─── Quality Gates (stg_sales_data_suite & fct_sales_suite)
 └──────┬───────────────┘
        │ Données validées à 100%
        ├─────────────────────────────┐
        ▼                             ▼
 ┌──────────────┐              ┌──────────────┐
 │    MLflow    │              │   Metabase   │
 │ Modélisation │              │ Visualisation│
 │ Time Series  │              │ Dashboard BI │
 └──────────────┘              └──────────────┘
        ▲                             ▲
        └──────────────┬──────────────┘
                       │ Orchestration de bout en bout
                ┌──────┴──────┐
                │   Dagster   │
                └─────────────┘
```

---

## 🛠️ Stack Technique & Rôles

* **Orchestration — [Dagster](https://dagster.io/) :** Automatise l'ordonnancement des tâches dans l'ordre requis, supervise les runs d'exécution et assure la traçabilité complète des assets.

* **Extraction & Ingestion — [Airbyte](https://airbyte.com/) :** Connecteur automatisé assurant le chargement périodique du fichier CSV source vers l'entrepôt PostgreSQL.

* **Stockage — [PostgreSQL](https://www.postgresql.org/) :** Base de données relationnelle hébergeant les tables brutes et les tables modélisées.

* **Transformation & Lignage — [dbt](https://www.getdbt.com/) :**

  * Nettoyage, standardisation des typologies et structuration modulaire.
  * Lignage de transformation : `raw_airbyte_sales_data` ➔ `stg_sales_data` ➔ `fct_sales`.

* **Validation Qualité — [Great Expectations](https://greatexpectations.io/) :**

  * Suites `stg_sales_data_suite` et `fct_sales_suite`.
  * Contrôle des contraintes d'intégrité : valeurs non nulles, types, montants ≥ 0, quantités et dates cohérentes.
  * Déclenchement automatique post-dbt via Dagster.
  * Taux de réussite : **100 %**.

* **Machine Learning & MLOps — [MLflow](https://mlflow.org/) :**

  * Entraînement et suivi de modèles prédictifs temporels (`TimeSeries_Models_Training`).
  * Suivi des paramètres, artefacts et métriques d'évaluation : RMSE, MAE.

* **Restitution Analytique — [Metabase](https://www.metabase.com/) :** Tableaux de bord interactifs de pilotage des ventes 2011 : suivi du chiffre d'affaires, panier moyen, volumes vendus et répartition géographique.

* **Conteneurisation — [Docker & Docker Compose](https://www.docker.com/) :** Déploiement reproductible de l'ensemble de l'écosystème.

---

## 📁 Structure du Répertoire

```text
data-lineage-engine/
│
├── airbyte/             # Configurations et exports des connexions Airbyte
├── dagster/             # Définition des jobs, ops, assets et schedules Dagster
├── dagster_home/        # Stockage local et configuration du daemon Dagster
├── dbt/                 # Projet dbt (modèles staging et mart fct_sales)
├── docker/              # Fichiers Dockerfile et scripts utilitaires
├── docs/                # Présentation technique et documentation du projet
├── gx/                  # Checkpoints, expectations suites et configurations Great Expectations
├── metabase_data/       # Persistance des configurations Metabase
├── ml/                  # Scripts de modélisation de séries temporelles
├── mlflow_db/           # Base SQLite de métadonnées pour MLflow
├── docker-compose.yml   # Fichier d'orchestration multi-conteneurs
├── run_dbt.ps1          # Script d'exécution rapide dbt
├── .gitignore           # Exclusion des fichiers générés et données lourdes
└── README.md
```

---

## ⚙️ Installation & Démarrage

### 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :

* Docker Desktop avec Docker Compose
* Python 3.9+
* Git

---

### 2. Cloner le projet

```bash
git clone https://github.com/walidlabied09/data-lineage-engine.git
cd data-lineage-engine
```

---

### 3. Démarrer l'infrastructure complète

L'ensemble des services est conteneurisé avec Docker Compose :

```bash
docker-compose up -d
```

Pour vérifier que les conteneurs sont bien démarrés :

```bash
docker-compose ps
```

---

## 🌐 Ports & Interfaces Web

| Service          | Rôle                                   | URL locale              |
| ---------------- | -------------------------------------- | ----------------------- |
| **Dagster UI**   | Orchestration & supervision des runs   | `http://localhost:3000` |
| **Airbyte**      | Gestion des flux d'ingestion           | `http://localhost:8000` |
| **Metabase**     | Tableaux de bord des ventes            | `http://localhost:3001` |
| **MLflow UI**    | Expérimentations de séries temporelles | `http://localhost:5001` |
| **GX Data Docs** | Rapports de qualité des données        | `http://localhost:8090` |

---

## 🔄 Exécution Manuelle des Composants

### Transformations SQL — dbt

Depuis le dossier `dbt/` :

```bash
cd dbt
dbt run
dbt test
```

---

### Validation des Données — Great Expectations

Depuis le dossier `gx/` :

```bash
cd gx
great_expectations checkpoint run sales_checkpoint
```

---

### Entraînement Machine Learning — MLflow

Depuis le dossier `ml/` :

```bash
cd ml
python train_timeseries.py
```

---

## 🔗 Flux de Données

Le traitement des données suit le flux suivant :

```text
Dataset CSV
     │
     ▼
  Airbyte
     │
     ▼
 PostgreSQL
     │
     ▼
    dbt
     │
     ▼
stg_sales_data
     │
     ▼
Great Expectations
     │
     ▼
  fct_sales
     │
     ├──────────────────────┐
     ▼                      ▼
  MLflow                Metabase
     │                      │
     ▼                      ▼
Prévisions              Dashboard
temporelles             décisionnel
```

---

## 📊 Qualité des Données

Great Expectations intervient comme **Quality Gate** dans le pipeline.

Les contrôles portent notamment sur :

* Les valeurs non nulles
* Les types de données
* Les montants
* Les quantités
* Les dates
* Les contraintes d'intégrité

Les suites de validation utilisées sont :

```text
stg_sales_data_suite
fct_sales_suite
```

Le pipeline est configuré pour déclencher automatiquement les contrôles de qualité après les transformations dbt.

---

## 🤖 Machine Learning & MLOps

Le projet intègre **MLflow** pour le suivi des expérimentations de Machine Learning.

Le module de modélisation permet d'effectuer des entraînements sur des **séries temporelles**.

Nom du processus d'entraînement :

```text
TimeSeries_Models_Training
```

Les éléments suivis avec MLflow comprennent notamment :

* Paramètres des modèles
* Métriques d'évaluation
* Artefacts
* Résultats des expérimentations

Les principales métriques utilisées sont :

```text
RMSE
MAE
```

---

## 📈 Business Intelligence

**Metabase** est utilisé pour la restitution et la visualisation des données de ventes.

Les tableaux de bord permettent notamment de suivre :

* 💰 Chiffre d'affaires
* 🛒 Panier moyen
* 📦 Volumes vendus
* 🌍 Répartition géographique
* 📅 Évolution des ventes

Les données analysées concernent notamment les ventes de **2011**.

---

## 🐳 Conteneurisation

L'ensemble de l'écosystème est conteneurisé avec **Docker** et **Docker Compose**.

Cette approche permet :

* Un environnement reproductible
* Un déploiement simplifié
* Une isolation des services
* Une gestion centralisée de l'infrastructure
* Un démarrage simultané des différents composants

Le fichier principal d'orchestration est :

```text
docker-compose.yml
```

---

## 🎯 Objectifs du Projet

Les principaux objectifs de cette plateforme sont :

* Automatiser l'ingestion des données
* Centraliser les données dans PostgreSQL
* Transformer les données avec dbt
* Garantir leur qualité avec Great Expectations
* Orchestrer l'ensemble du pipeline avec Dagster
* Entraîner des modèles prédictifs avec MLflow
* Restituer les indicateurs dans Metabase
* Mettre en place une architecture Data moderne et reproductible

---

## 👥 Auteurs & Encadrement

Projet réalisé dans le cadre du cycle d'ingénieur **Big Data Engineering** à l'**Université Internationale de Rabat (UIR)**.

### Étudiants

* **Adam Amara**
* **Saad Gaga**
* **Walid Labied**
* **Othmane Lemjid**

### Encadrant pédagogique

* **M. Youssef Gahi**

---

## 📌 Résumé de l'Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                     MODERN DATA STACK                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  CSV                                                         │
│   │                                                          │
│   ▼                                                          │
│ Airbyte ───────► PostgreSQL                                  │
│                      │                                       │
│                      ▼                                       │
│                     dbt                                      │
│                      │                                       │
│                      ▼                                       │
│             Great Expectations                               │
│                      │                                       │
│              ┌───────┴────────┐                              │
│              ▼                ▼                              │
│           MLflow          Metabase                            │
│              │                │                              │
│              ▼                ▼                              │
│       Machine Learning    Dashboard BI                       │
│                                                              │
│                 ↑                                            │
│                 │                                            │
│              Dagster                                         │
│        Orchestration globale                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📜 Licence

Ce projet a été réalisé dans un cadre académique dans le cadre du cycle d'ingénieur **Big Data Engineering** à l'**Université Internationale de Rabat (UIR)**.

Toute utilisation, modification ou redistribution du projet doit respecter les conditions définies par ses auteurs.
