import time

from gustavo_sdk.app.jobs.mysql_to_bucket import MySQLToBucketJob
from gustavo_sdk.app.jobs.postgre_to_bucket import PostgresToBucketJob
from gustavo_sdk.infrastructure.common.config.settings import Settings
from gustavo_sdk.infrastructure.common.utils import get_logger
from gustavo_sdk.infrastructure.integration.databases.mysql_client import MySQLClient
from gustavo_sdk.infrastructure.integration.databases.postgres_client import PostgresClient

logger = get_logger(__name__)


def mysql_to_bucket() -> None:
    start_time = time.time()
    status = "SUCCESS"
    db = None

    try:
        settings = Settings()
        db = MySQLClient(config=settings.get_mysql_config())
        db.connect()

        job = MySQLToBucketJob(db=db)

        job.run(
            query="SELECT * FROM clientes",
            file_name="clientes.csv",
        )

    except Exception as err:
        status = "FAILED"
        logger.exception(f"ETL job failed: {err}")

    finally:
        if db is not None:
            db.close()

        duration = time.time() - start_time
        logger.info(f"Status: {status} | Duration: {duration:.2f}s")


def postgres_to_bucket() -> None:
    start_time = time.time()
    status = "SUCCESS"
    db = None

    try:
        settings = Settings()
        db = PostgresClient(config=settings.get_postgres_config())
        db.connect()

        job = PostgresToBucketJob(db=db)

        job.run(
            query="SELECT * FROM clientes",
            file_name="clientes_postgres.csv",
        )

    except Exception as err:
        status = "FAILED"
        logger.exception(f"PostgreSQL ETL job failed: {err}")

    finally:
        if db is not None:
            db.close()

        duration = time.time() - start_time
        logger.info(f"Status: {status} | Duration: {duration:.2f}s")

