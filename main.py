import time
from core.logger import get_logger
from config.settings import Settings
from integration.databases.mysql_client import MySQLClient
from writers.filewriter import FileWriter
from app.jobs.mysql_to_bucket.job import MySQLToBucketJob

logger = get_logger(__name__)


def main() -> None:
    start = time.time()
    db = None

    try:
        settings = Settings()

        db = MySQLClient(settings.get_mysql_config())
        db.connect()

        job = MySQLToBucketJob(
            db=db,
            writer=FileWriter(settings.output_path)
        )

        job.run(
            query="SELECT * FROM clientes",
            file_name="clientes.csv"
        )

    except Exception as e:
        logger.exception(f"ETL failed: {e}")

    finally:
        if db:
            db.close()

        logger.info(f"Finished in {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()