FROM python:3.10-slim

WORKDIR /usr/src/app

# Installer Great Expectations + Postgres
RUN pip install --no-cache-dir \
    "great_expectations[postgresql]==1.9.0" \
    pandas \
    sqlalchemy \
    psycopg2-binary

# ❗ Garde le conteneur en vie en suivant un fichier qui n'arrête jamais
CMD ["tail", "-f", "/dev/null"]
