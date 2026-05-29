import time

from app.jobs.mysql_to_bucket import MySQLToBucketJob
from config.settings import Settings
from core.logger import get_logger
from integration.databases.mysql_client import MySQLClient
from writers.file_writer import FileWriter

logger = get_logger(__name__)


def main() -> None:
    start_time = time.time()
    status = "SUCCESS"

    db: MySQLClient | None = None

    try:
        settings = Settings()

        db = MySQLClient(
            config=settings.get_mysql_config()
        )

        db.connect()

        job = MySQLToBucketJob(
            db=db,
            writer=FileWriter(
                output_path=settings.output_path
            ),
        )

        job.run(
            query="SELECT * FROM clientes",
            file_name="clientes.csv",
        )

    except Exception:
        status = "FAILED"
        logger.exception("ETL job failed")

    finally:
        if db:
            db.close()

        duration = time.time() - start_time

        logger.info(
            f"Status: {status} | Duration: {duration:.2f}s"
        )


if __name__ == "__main__":
    main()