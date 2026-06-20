from datetime import datetime
from pathlib import Path

import pandas as pd

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from gustavo_sdk.infrastructure.common.utils import get_logger



logger = get_logger(__name__)

POSTGRES_CONN_ID = "postgres_default"

LANDING_DIR = Path("/opt/airflow/landing")
LANDING_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def extract_table(
    table_name: str,
    output_file: str,
) -> pd.DataFrame:
    try:
        logger.info(
            f"Starting extraction from table {table_name}"
        )

        hook = PostgresHook(
            postgres_conn_id=POSTGRES_CONN_ID
        )

        dataframe = hook.get_pandas_df(
            f"SELECT * FROM {table_name}"
        )

        output_path = LANDING_DIR / output_file

        dataframe.to_csv(
            output_path,
            index=False,
        )

        logger.info(
            f"File saved successfully: {output_path}"
        )

        return dataframe

    except Exception as error:
        logger.exception(
            f"Failed extracting table {table_name}"
        )

        raise RuntimeError(
            f"Error extracting table {table_name}"
        ) from error


def extract_user() -> pd.DataFrame:
    return extract_table(
        table_name="usuario",
        output_file="usuarios.csv",
    )


def extract_product() -> pd.DataFrame:
    return extract_table(
        table_name="produto",
        output_file="produtos.csv",
    )


def save_user() -> None:
    pass


def save_product() -> None:
    pass


with DAG(
    dag_id="postgres_ingestion",
    start_date=datetime(2026, 6, 14),
    schedule=None,
    catchup=False,
) as dag:

    extract_user_task = PythonOperator(
        task_id="extract_user",
        python_callable=extract_user,
    )

    save_user_task = PythonOperator(
        task_id="save_user",
        python_callable=save_user,
    )

    extract_product_task = PythonOperator(
        task_id="extract_product",
        python_callable=extract_product,
    )

    save_product_task = PythonOperator(
        task_id="save_product",
        python_callable=save_product,
    )

    extract_user_task >> save_user_task
    extract_product_task >> save_product_task