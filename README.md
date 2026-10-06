# 🔄 Pipeline ETL & Machine Learning Orchestré — Modern Data Stack

Plateforme automatisée de bout en bout conçue pour collecter, transformer, valider et exploiter des données transactionnelles de ventes, depuis l'ingestion des données brutes jusqu'à la modélisation prédictive et à la restitution décisionnelle.

---

## 🏗️ Architecture Globale du Pipeline

Le pipeline est entièrement orchestré par **Dagster** et s'articule autour d'une base **PostgreSQL**.

```text
                         ┌──────────────┐
                         │ Dataset CSV  │
                         │ Données      │
                         │ de ventes    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Airbyte    │
                         │  Ingestion   │
                         └──────┬───────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │      PostgreSQL        │
                    │   Stockage central     │
                    │    Raw & Transformed   │
                    └───────────┬────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │     dbt      │
                         │ Transformation│
                         └──────┬───────┘
                                │
                                ▼
                  ┌──────────────────────────┐
                  │  Great Expectations      │
                  │     Quality Gates        │
                  └────────────┬─────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │    MLflow    │      │   Metabase   │
             │  Machine     │      │  Dashboard   │
             │  Learning    │      │      BI      │
             └──────────────┘      └──────────────┘

                         ▲
                         │
                  ┌──────┴──────┐
                  │   Dagster   │
                  │Orchestration│
                  └─────────────┘
```

---

## 🛠️ Stack Technique & Rôles

### 🔄 Orchestration — Dagster

* Automatisation et ordonnancement des tâches.
* Supervision des runs d'exécution.
* Gestion des assets et dépendances.
* Traçabilité du pipeline de bout en bout.

### 📥 Extraction & Ingestion — Airbyte

* Chargement automatisé du fichier CSV source.
* Ingestion vers PostgreSQL.
* Gestion des flux de données.

### 🗄️ Stockage — PostgreSQL

Base de données relationnelle centrale contenant les données brutes et transformées.

### 🔧 Transformation — dbt

* Nettoyage et standardisation des données.
* Transformation SQL modulaire.
* Construction des modèles analytiques.
* Lignage :

```text
raw_airbyte_sales_data
          │
          ▼
   stg_sales_data
          │
          ▼
      fct_sales
```

### ✅ Validation Qualité — Great Expectations

Suites de validation utilisées :

* `stg_sales_data_suite`
* `fct_sales_suite`

Contrôles réalisés notamment sur :

* Valeurs non nulles.
* Types de données.
* Montants supérieurs ou égaux à zéro.
* Quantités.
* Dates.
* Contraintes d'intégrité.

Les contrôles qualité sont déclenchés automatiquement après les transformations dbt via Dagster.

### 🤖 Machine Learning & MLOps — MLflow

* Entraînement de modèles prédictifs sur séries temporelles.
* Suivi des expérimentations.
* Suivi des paramètres.
* Suivi des métriques.
* Gestion des artefacts et modèles.

Métriques utilisées :

* RMSE
* MAE

### 📊 Business Intelligence — Metabase

Tableaux de bord interactifs permettant d'analyser les ventes :

* Chiffre d'affaires.
* Panier moyen.
* Volumes vendus.
* Répartition géographique.
* Évolution mensuelle des ventes.

### 🐳 Conteneurisation — Docker

L'ensemble de l'écosystème est déployé avec **Docker et Docker Compose** afin de garantir un environnement reproductible et facilement déployable.

---

## 📁 Structure du Répertoire

```text
data-lineage-engine/
│
├── airbyte/             # Configurations et exports des connexions Airbyte
├── dagster/             # Jobs, ops, assets et schedules Dagster
├── dagster_home/        # Configuration et stockage local Dagster
├── dbt/                 # Projet dbt et modèles SQL
├── docker/              # Dockerfiles et scripts utilitaires
├── docs/                # Documentation technique
├── gx/                  # Great Expectations
├── metabase_data/       # Données persistantes Metabase
├── ml/                  # Scripts Machine Learning
├── mlflow_db/           # Base de métadonnées MLflow
│
├── docker-compose.yml   # Orchestration des conteneurs
├── run_dbt.ps1          # Script d'exécution dbt
├── .gitignore           # Fichiers exclus du dépôt
└── README.md            # Documentation du projet
```

---

## ⚙️ Installation & Démarrage

### 1. Prérequis

Avant de commencer, installez :

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Docker Compose
* Python 3.9+
* Git

### 2. Cloner le projet

```bash
git clone https://github.com/walidlabied09/data-lineage-engine.git
cd data-lineage-engine
```

### 3. Démarrer l'infrastructure

L'ensemble des services est conteneurisé avec Docker Compose.

```bash
docker-compose up -d
```

### 4. Vérifier les conteneurs

```bash
docker-compose ps
```

---

## 🌐 Ports & Interfaces Web

| Service          | Rôle                         | URL locale              |
| ---------------- | ---------------------------- | ----------------------- |
| **Dagster UI**   | Orchestration et supervision | `http://localhost:3000` |
| **Airbyte**      | Gestion de l'ingestion       | `http://localhost:8000` |
| **Metabase**     | Dashboards BI                | `http://localhost:3001` |
| **MLflow UI**    | Suivi Machine Learning       | `http://localhost:5001` |
| **GX Data Docs** | Rapports de qualité          | `http://localhost:8090` |

---

## 🔄 Exécution Manuelle des Composants

### Transformation avec dbt

```bash
cd dbt

dbt run
dbt test
```

### Validation avec Great Expectations

```bash
cd gx

great_expectations checkpoint run sales_checkpoint
```

### Entraînement Machine Learning

```bash
cd ml

python train_timeseries.py
```

---

## 🔗 Flux de Données

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
                    ┌────┴────┐
                    ▼         ▼
                 MLflow    Metabase
                    │         │
                    ▼         ▼
              Prévisions  Dashboard
              temporelles  décisionnel
```

---

## 📊 Qualité des Données

**Great Expectations** intervient comme **Quality Gate** dans le pipeline.

Les contrôles portent notamment sur :

* Valeurs non nulles.
* Types de données.
* Montants.
* Quantités.
* Dates.
* Contraintes d'intégrité.

### Suites de validation

```text
stg_sales_data_suite
fct_sales_suite
```

Le pipeline déclenche automatiquement les contrôles de qualité après les transformations dbt.

---

## 🤖 Machine Learning & MLOps

Le projet intègre **MLflow** pour le suivi des expérimentations de Machine Learning sur des séries temporelles.

Expérience principale :

```text
TimeSeries_Models_Training
```

Les éléments suivis avec MLflow comprennent :

* Paramètres des modèles.
* Métriques d'évaluation.
* Artefacts.
* Modèles.
* Runs d'entraînement.

### Métriques

* **RMSE** — Root Mean Squared Error
* **MAE** — Mean Absolute Error

---

## 📈 Business Intelligence

**Metabase** est utilisé pour la restitution et la visualisation des données de ventes 2011.

Les principaux indicateurs comprennent :

* 💰 Chiffre d'affaires
* 🛒 Panier moyen
* 📦 Volumes vendus
* 🌍 Répartition géographique
* 📅 Évolution mensuelle des ventes

---

## 🐳 Conteneurisation

L'ensemble de l'écosystème est conteneurisé via :

```text
docker-compose.yml
```

### Avantages

* Environnement isolé.
* Déploiement reproductible.
* Déploiement multi-services simplifié.
* Gestion centralisée des réseaux.
* Gestion des volumes persistants.

---

## 🎯 Objectifs du Projet

Ce projet a pour objectifs de :

* Automatiser l'ingestion des données transactionnelles.
* Centraliser les données dans PostgreSQL.
* Transformer les données avec dbt.
* Garantir la qualité des données avec Great Expectations.
* Orchestrer l'ensemble du pipeline avec Dagster.
* Entraîner des modèles prédictifs avec MLflow.
* Restituer les indicateurs décisionnels avec Metabase.
* Mettre en place une architecture moderne de traitement de données.

---

## 👥 Auteurs & Encadrement

Projet réalisé dans le cadre du cycle d'ingénieur **Big Data Engineering** à l'**Université Internationale de Rabat (UIR)**.

### Étudiants

* **Adam Amara**
* **Saad Gaga**
* **Walid Labied**
* **Othmane Lemjid**

### Encadrant pédagogique

**M. Youssef Gahi**

---

## 🧩 Architecture Finale

```text
┌──────────────────────────────────────────────────────────────┐
│                    MODERN DATA STACK                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                         CSV                                  │
│                          │                                   │
│                          ▼                                   │
│                       Airbyte                                │
│                          │                                   │
│                          ▼                                   │
│                     PostgreSQL                               │
│                          │                                   │
│                          ▼                                   │
│                         dbt                                  │
│                          │                                   │
│                          ▼                                   │
│                 Great Expectations                            │
│                          │                                   │
│                   ┌──────┴──────┐                            │
│                   ▼             ▼                            │
│                MLflow       Metabase                         │
│                   │             │                            │
│                   ▼             ▼                            │
│             Machine Learning  Dashboard BI                   │
│                                                              │
│                          ▲                                   │
│                          │                                   │
│                       Dagster                                │
│                 Orchestration globale                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📜 Licence

Ce projet a été réalisé dans un cadre académique à l'**Université Internationale de Rabat (UIR)**.

Toute utilisation, modification ou redistribution doit respecter les conditions définies par les auteurs.
