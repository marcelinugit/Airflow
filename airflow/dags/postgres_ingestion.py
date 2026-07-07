from datetime import datetime
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import json

from gustavo_sdk.app.airflow_functions import postgres_to_bucket

logger = logging.getLogger(__name__)

conn_postgres = BaseHook.get_connection("postgres_default")
host = conn_postgres.host
user = conn_postgres.login
password = conn_postgres.password
port = conn_postgres.port or 3306
database = conn_postgres.schema

conn_bq = BaseHook.get_connection("gcp_default")
service_account_info = json.loads(
    conn_bq.extra_dejson["keyfile_dict"]
)

today = datetime.now()

ano = today.year
mes = f"{today.month:02d}"
dia = f"{today.day:02d}"

hive_partition = (
        f"partition_year={ano}/"
        f"partition_month={mes}/"
        f"partition_day={dia}"
)

with DAG(
    dag_id="ingestion_postgres_ifood_landing",
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
            "bucket_name": "ifood-data-lake",
            "bucket_prefix": f"ifood/usuario/{hive_partition}",
            "credentials_json": service_account_info,
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
            "bucket_name": "ifood-data-lake",
            "bucket_prefix": f"ifood/produto/{hive_partition}",
            "credentials_json": service_account_info,
        }
    )