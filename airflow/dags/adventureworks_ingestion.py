import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
import json

from gustavo_sdk.app.airflow_functions import postgres_to_bucket

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
            "file_name": f"adventureworks_customer_{timestamp}.parquet",
            "bucket_name": "ifood-data-lake",
            "bucket_prefix": (
                f"adventureworks/customer/{hive_partition}"
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
            "file_name": f"adventureworks_product_{timestamp}.parquet",
            "bucket_name": "ifood-data-lake",
            "bucket_prefix": (
                f"adventureworks/product/{hive_partition}"
            ),
            "credentials_json": service_account_info,
        },
    )