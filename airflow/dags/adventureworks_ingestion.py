import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import json

from gustavo_sdk.app.airflow_functions import (
    postgres_to_bucket,
    run_raw,
)

logger = logging.getLogger(__name__)


conn_postgres = BaseHook.get_connection("adventureworks_postgres")

host = conn_postgres.host
user = conn_postgres.login
password = conn_postgres.password
port = conn_postgres.port or 5432
database = conn_postgres.schema


conn_bq = BaseHook.get_connection("gcp_default")

service_account_info = json.loads(
    conn_bq.extra_dejson["keyfile_dict"]
)

project_id = service_account_info["project_id"]
system = "adventureworks"
schema = "adventureworks_raw"
bucket_name = "gustavo-data-plataform-raw"

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
    dag_id="ingestion_postgres_adventureworks_landing",
    start_date=datetime(2026, 8, 22),
    schedule=None,
    catchup=False,
) as dag:

    customer_ingestion = PythonOperator(
        task_id="customer_ingestion",
        python_callable=postgres_to_bucket,
        op_kwargs={
            "host": host,
            "user": user,
            "password": password,
            "port": port,
            "database": database,
            "table_name": "Sales.Customer",
            "bucket_name": bucket_name,
            "bucket_prefix": (
                f"{system}/customer/{hive_partition}"
            ),
            "credentials_json": service_account_info,
        },
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
            "table_name": "Production.Product",
            "bucket_name": bucket_name,
            "bucket_prefix": (
                f"{system}/product/{hive_partition}"
            ),
            "credentials_json": service_account_info,
        },
    )

    customer_raw = PythonOperator(
        task_id="customer_raw",
        python_callable=run_raw,
        op_kwargs={
            "project_id": project_id,
            "schema": schema,
            "system": system,
            "table": "customer",
            "bucket_name": bucket_name,
            "year": str(ano),
            "month": mes,
            "day": dia,
            "credentials_json": service_account_info,
        },
    )

    product_raw = PythonOperator(
        task_id="product_raw",
        python_callable=run_raw,
        op_kwargs={
            "project_id": project_id,
            "schema": schema,
            "system": system,
            "table": "product",
            "bucket_name": bucket_name,
            "year": str(ano),
            "month": mes,
            "day": dia,
            "credentials_json": service_account_info,
        },
    )

    customer_ingestion >> customer_raw
    product_ingestion >> product_raw
    customer_raw >> product_raw