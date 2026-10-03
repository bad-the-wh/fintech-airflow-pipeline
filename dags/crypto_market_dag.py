from datetime import datetime, timedelta
import sys
import os
import logging

from airflow.decorators import dag, task

# Ensure Airflow can locate modules inside the 'include' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../include')))

from extract import fetch_crypto_market_data
from transform import transform_crypto_data
from data_quality import run_data_quality_checks
from load import load_crypto_data_to_postgres

logger = logging.getLogger(__name__)

def task_failure_alert_callback(context):
    """
    Production alerting hook. In a corporate setup, this would format 
    and push an alert payload to a Slack Webhook or PagerDuty API.
    """
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    execution_date = context.get('execution_date')
    
    logger.error(
        f"🚨 [ALERT] Pipeline Failure Detected! \n"
        f" - DAG: {dag_id}\n"
        f" - Task: {task_id}\n"
        f" - Execution Time: {execution_date}\n"
        f"Action required: Check Airflow task logs immediately."
    )

default_args = {
    'owner': 'data_engineer',
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'on_failure_callback': task_failure_alert_callback,
}

@dag(
    dag_id='fintech_crypto_market_etl',
    default_args=default_args,
    description='Production-grade fintech ETL pipeline with data quality gates and failure alerts',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['fintech', 'crypto', 'etl', 'production'],
)
def crypto_etl_pipeline():

    @task(task_id='extract_market_data')
    def extract():
        return fetch_crypto_market_data(per_page=20)

    @task(task_id='transform_market_data')
    def transform(raw_data: list):
        return transform_crypto_data(raw_data)

    @task(task_id='run_data_quality_validations')
    def quality_checks(transformed_data: list):
        run_data_quality_checks(transformed_data)
        return transformed_data  # Pass through on success

    @task(task_id='load_market_data')
    def load(clean_data: list):
        load_crypto_data_to_postgres(clean_data)

    # Define robust pipeline dependency flow with data quality gateway
    raw_json = extract()
    clean_data = transform(raw_json)
    validated_data = quality_checks(clean_data)
    load(validated_data)

dag_instance = crypto_etl_pipeline()