import subprocess
from dagster import op, get_dagster_logger
import os

DBT_DIR = "/usr/app"

@op
def dbt_run_op():
    logger = get_dagster_logger()

    if not os.path.exists(DBT_DIR):
        raise Exception(f"❌ DBT folder not found: {DBT_DIR}")

    logger.info("🚀 Running dbt run + dbt test...")

    command = f"cd {DBT_DIR} && dbt run --no-partial-parse && dbt test --no-partial-parse"

    process = subprocess.Popen(
        ["bash", "-lc", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    output_lines = []

    for line in process.stdout:
        clean = line.rstrip()
        output_lines.append(clean)
        logger.info(clean)

    process.wait()

    # Sauvegarder aussi les logs dans un fichier
    with open(f"{DBT_DIR}/dbt_dagster.log", "w") as f:
        f.write("\n".join(output_lines))

    if process.returncode != 0:
        raise Exception("❌ dbt failed (check logs in /usr/app/dbt_dagster.log)")

    logger.info("✅ DBT completed successfully (run + test)")
