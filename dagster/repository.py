from dagster import Definitions

from jobs.data_quality_job import data_quality_job
from ops.airbyte_op import airbyte_sync_op
from ops.dbt_op import dbt_run_op
from ops.gx_op import gx_validation_op

# Petit job test
from dagster import op, job

@op
def hello_op():
    print("✓ Dagster fonctionne (hello_job)")

@job
def hello_job():
    hello_op()

# Repository FINAL
defs = Definitions(
    jobs=[
        hello_job,
        data_quality_job
    ]
)
