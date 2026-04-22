from dagster import job
from ops.airbyte_op import airbyte_sync_op
from ops.dbt_op import dbt_run_op
from ops.gx_op import gx_validation_op

@job
def data_quality_job():
    airbyte_sync_op()
    dbt_run_op()
    gx_validation_op()
