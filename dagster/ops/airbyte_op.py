import os
import time
import requests
from dagster import op, get_dagster_logger


@op
def airbyte_sync_op():
    logger = get_dagster_logger()

    base_url = os.getenv("AIRBYTE_URL")          # ex: http://host.docker.internal:8000/api/v1
    connection_id = os.getenv("AIRBYTE_CONNECTION_ID")
    username = os.getenv("AIRBYTE_USERNAME")
    password = os.getenv("AIRBYTE_PASSWORD")

    if not base_url or not connection_id or not username or not password:
        raise Exception("⚠️ AIRBYTE_URL, AIRBYTE_CONNECTION_ID, AIRBYTE_USERNAME ou AIRBYTE_PASSWORD manquant dans l'env")

    auth = (username, password)

    # 1️⃣ Créer un job de type sync
    logger.info(f"🚀 Lancement du sync Airbyte pour la connexion {connection_id}")

    trigger = requests.post(
        f"{base_url}/jobs",
        json={"jobType": "sync", "connectionId": connection_id},
        auth=auth,
        timeout=60,
    )

    if trigger.status_code != 200:
        raise Exception(f"❌ Erreur API Airbyte (sync): {trigger.text}")

    job = trigger.json()
    job_id = job.get("id") or job.get("jobId")
    logger.info(f"✅ Job Airbyte créé : {job_id}")

    # 2️⃣ Poller le statut du job jusqu'à ce qu'il termine
    while True:
        status_resp = requests.get(
            f"{base_url}/jobs/{job_id}",
            auth=auth,
            timeout=30,
        )
        if status_resp.status_code != 200:
            raise Exception(f"❌ Erreur API Airbyte (job status): {status_resp.text}")

        status = status_resp.json().get("status")
        logger.info(f"⏱️ Statut job Airbyte {job_id}: {status}")

        if status in ("succeeded", "failed", "cancelled", "incomplete"):
            break

        time.sleep(5)

    if status != "succeeded":
        raise Exception(f"❌ Sync Airbyte terminé avec le statut : {status}")

    logger.info("🎉 Sync Airbyte terminé avec succès")
