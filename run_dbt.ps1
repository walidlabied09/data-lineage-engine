# run_dbt.ps1

# 1) démarre le conteneur dbt
docker compose up -d

# 2) assure que le Postgres Airbyte est sur le bon réseau (idempotent)
docker network connect airbyte_default postgres-airbyte 2>$null

# 3) build + tests
docker compose exec dbt sh -c "cd /usr/app && dbt deps && dbt run && dbt test"
