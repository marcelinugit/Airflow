from datetime import datetime
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook

from gustavo_sdk.app.airflow_functions import postgres_to_bucket

logger = logging.getLogger(__name__)

conn = BaseHook.get_connection("postgres_default")
host = conn.host
user = conn.login
password = conn.password
port = conn.port or 3306
database = conn.schema

with DAG(
    dag_id="ingestion_postgres_ecomercegustavo_landing",
    start_date=datetime(2026, 6, 14),
    schedule=None,
    catchup=False,
) as dag:

    user_ingestion = PythonOperator(
        task_id="user_ingestion",
        python_callable=postgres_to_bucket,
        op_kwargs={
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "database": database,
            "table_name": "usuario",
            "bucket_prefix": "ecomercegustavo/usuario/data.csv",
        }
    )

    product_ingestion = PythonOperator(
        task_id="product_ingestion",
        python_callable=postgres_to_bucket,
        op_kwargs={
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "database": database,
            "table_name": "produto",
            "bucket_prefix": "ecomercegustavo/produto/data.csv",
        }
    )