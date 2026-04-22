FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure pip
ENV PIP_DEFAULT_TIMEOUT=1000 \
    PIP_RETRIES=5 \
    PIP_NO_CACHE_DIR=1

RUN pip install --upgrade setuptools wheel

# Install Dagster + dbt
RUN pip install \
    dagster \
    dagster-webserver \
    dagster-dbt \
    dbt-postgres==1.9.1 \
    psycopg2-binary \
    requests

# ⬇️ **MANQUAIT !! Installe Great Expectations**
RUN pip install "great_expectations[postgresql]==1.9.0"


# Copy Dagster project
WORKDIR /opt/dagster
COPY . /opt/dagster

# Copy DBT project
RUN mkdir -p /usr/app && cp -r /opt/dagster/dbt/. /usr/app/

# Install dbt deps INSIDE /usr/app
RUN dbt deps --project-dir /usr/app || true

ENV DAGSTER_HOME=/opt/dagster_home
CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000"]
