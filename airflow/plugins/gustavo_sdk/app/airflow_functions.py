from gustavo_sdk.app.jobs.mysql_to_bucket import MySQLToBucketJob
from gustavo_sdk.app.jobs.postgre_to_bucket import PostgresToBucketJob
from gustavo_sdk.infrastructure.common.utils import get_logger
from gustavo_sdk.infrastructure.integration.databases.mysql_client import MySQLClient
from gustavo_sdk.infrastructure.integration.databases.postgres_client import PostgresClient
from gustavo_sdk.app.jobs.pipelines.raw import Raw
from gustavo_sdk.app.jobs.pipelines.bronze import Bronze


logger = get_logger(__name__)


def mysql_to_bucket(
        table_name: str,
        bucket_name: str,
        bucket_prefix: str,
        host: str,
        database: str,
        user: str,
        password: str,
        port: str,
        credentials_json: str,
) -> None:
    try:
        config = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
        }

        db = MySQLClient(
            config=config
        )

        db.connect()

        job = MySQLToBucketJob(
            db=db,
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            credentials_json=credentials_json,
        )

        job.run(
            query=f"SELECT * FROM {table_name}",
        )

    except Exception as err:
        logger.exception(f"MySQL ETL job failed: {err}")
        raise


def postgres_to_bucket(
        table_name: str,
        bucket_name: str,
        bucket_prefix: str,
        host: str,
        database: str,
        user: str,
        password: str,
        port: str,
        credentials_json: str,
) -> None:
    try:
        config = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
        }

        db = PostgresClient(
            config=config
        )

        db.connect()

        job = PostgresToBucketJob(
            db=db,
            bucket_name=bucket_name,
            bucket_prefix=bucket_prefix,
            credentials_json=credentials_json,
        )

        job.run(
            query=f"SELECT * FROM {table_name}",
        )

    except Exception as err:
        logger.exception(f"PostgreSQL ETL job failed: {err}")
        raise


def run_raw(
        project_id: str,
        schema: str,
        system: str,
        table: str,
        bucket_name: str,
        year: str,
        month: str,
        day: str,
        credentials_json: dict,
) -> None:
    raw = Raw(
        project_id=project_id,
        schema=schema,
        system=system,
        table=table,
        bucket_name=bucket_name,
        year=year,
        month=month,
        day=day,
        credentials_json=credentials_json,
    )

    raw.run()


def run_bronze(
        project_id: str,
        system: str,
        table: str,
        pk: str,
        credentials_json: dict,
) -> None:
    bronze = Bronze(
        project_id=project_id,
        system=system,
        table=table,
        pk=pk,
        credentials_json=credentials_json,
    )

    bronze.run()