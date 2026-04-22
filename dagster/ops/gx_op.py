# dagster/ops/gx_op.py
import subprocess
from dagster import op, get_dagster_logger

@op
def gx_validation_op():
    logger = get_dagster_logger()
    logger.info("▶️ Running Great Expectations pipeline...")

    cmd = ["bash", "-lc", "cd /usr/app && python gx/gx_pipeline.py"]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    all_output = []

    # stream live logs into Dagster
    for line in process.stdout:
        line = line.rstrip()
        all_output.append(line)
        logger.info(line)

    process.wait()

    # save logs for debugging
    log_path = "/usr/app/gx_dagster.log"
    with open(log_path, "w") as f:
        f.write("\n".join(all_output))

    if process.returncode != 0:
        logger.error(f"GE exited with code {process.returncode}")
        raise Exception("❌ Great Expectations failed — see gx_dagster.log")

    logger.info("✅ Great Expectations validation OK")
