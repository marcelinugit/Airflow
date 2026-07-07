from gustavo_sdk.app.jobs.mysql_to_bucket import MySQLToBucketJob
from gustavo_sdk.app.jobs.postgre_to_bucket import PostgresToBucketJob
from gustavo_sdk.infrastructure.common.utils import get_logger
from gustavo_sdk.infrastructure.integration.databases.mysql_client import MySQLClient
from gustavo_sdk.infrastructure.integration.databases.postgres_client import PostgresClient

logger = get_logger(__name__)


def mysql_to_bucket(
        table_name: str,
        bucket_name: str,
        bucket_prefix: str,
        file_name: str,
        host: str,
        database: str,
        user: str,
        password: str,
        port: str,
        credentials_json: str,
) -> None:
    try:
        config = {
            "host":host,
            "database":database,
            "user":user,
            "password":password,
            "port":port,
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
            file_name=file_name,
        )
    except Exception as err:
        logger.exception(f"MySQL ETL job failed: {err}")
        raise


def postgres_to_bucket(
                        table_name: str,
                        bucket_name: str,
                        bucket_prefix: str,
                        file_name: str,
                        host: str,
                        database: str,
                        user: str,
                        password: str,
                        port: str,
                        credentials_json: str,
                        ) -> None:
    try:

        config = {
            "host":host,
            "database":database,
            "user":user,
            "password":password,
            "port":port,
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
            file_name=file_name,
        )

    except Exception as err:
        logger.exception(f"PostgreSQL ETL job failed: {err}")
        raise