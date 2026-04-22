FROM python:3.10-slim

WORKDIR /app

# ----------------------------------------------------
# Dépendances système MINIMALES
# ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# Mise à jour pip
# ----------------------------------------------------
RUN pip install --upgrade pip

# ----------------------------------------------------
# Installation Prophet SANS compilation (instantané)
# ----------------------------------------------------
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas \
    matplotlib \
    scikit-learn \
    mlflow \
    xgboost \
    sqlalchemy \
    psycopg2-binary \
    prophet==1.1.5 \
    cmdstanpy==1.2.3

# ----------------------------------------------------
# Copier le code
# ----------------------------------------------------
COPY ml/ /app/ml/

# ----------------------------------------------------
# Commande
# ----------------------------------------------------
CMD ["python", "/app/ml/train_all_models.py"]
