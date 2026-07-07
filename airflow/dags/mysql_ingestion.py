import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import json
from gustavo_sdk.app.airflow_functions import mysql_to_bucket

logger = logging.getLogger(__name__)

conn_mysql = BaseHook.get_connection("mysql_default")
host = conn_mysql.host
user = conn_mysql.login
password = conn_mysql.password
port = conn_mysql.port or 3306
database = conn_mysql.schema

conn_bq = BaseHook.get_connection("gcp_default")
service_account_info = json.loads(
    conn_bq.extra_dejson["keyfile_dict"]
)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

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
    dag_id="ingestion_mysql_mercadolivre_landing",
    start_date=datetime(2026, 6, 14),
    schedule=None,
    catchup=False,
) as dag:

    user_ingestion = PythonOperator(
        task_id="user_ingestion",
        python_callable=mysql_to_bucket,
        op_kwargs={
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "database": database,
            "table_name": "usuario",
            "file_name": f"usuario_{timestamp}.csv",
            "bucket_name": "mercadolivre-data-lake",
            "bucket_prefix": f"mercadolivre/usuario/{hive_partition}",
            "credentials_json": service_account_info,
        }
    )

    product_ingestion = PythonOperator(
        task_id="product_ingestion",
        python_callable=mysql_to_bucket,
        op_kwargs={
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "database": database,
            "table_name": "produto",
            "file_name": f"produto_{timestamp}.csv",
            "bucket_name": "mercadolivre-data-lake",
            "bucket_prefix": f"mercadolivre/produto/{hive_partition}",
            "credentials_json": service_account_info,
        }
    )