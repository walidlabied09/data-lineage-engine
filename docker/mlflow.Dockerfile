FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --no-cache-dir \
    numpy pandas matplotlib scikit-learn \
    mlflow==2.11.1 \
    psutil \
    torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu \
    xgboost orbit-ml

COPY ml/ /app/ml/

CMD ["python", "/app/ml/train_all_models.py"]
