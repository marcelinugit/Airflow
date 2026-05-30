import time

from app.jobs.postgre_to_bucket import PostgresToBucketJob
from config.settings import Settings
from core.logger import get_logger
from integration.databases.postgres_client import PostgresClient
from writers.file_writer import FileWriter

logger = get_logger(__name__)


def main() -> None:
    start_time = time.time()
    status = "SUCCESS"

    settings = Settings()

    db = PostgresClient(
        config=settings.get_postgres_config()
    )

    try:
        db.connect()

        writer = FileWriter(
            output_path=settings.output_path
        )

        job = PostgresToBucketJob(
            db=db,
            writer=writer,
        )

        job.run(
            query="SELECT * FROM clientes",
            file_name="clientes_postgres.csv",
        )

    except Exception:
        status = "FAILED"
        logger.exception("PostgreSQL ETL job failed")

    finally:
        db.close()

        duration = time.time() - start_time

        logger.info(
            f"Status: {status} | Duration: {duration:.2f}s"
        )


if __name__ == "__main__":
    main()