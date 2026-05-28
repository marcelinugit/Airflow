import time
import logging

from src.config.settings import Settings
from src.clients.mysql_client import MySQLClient
from src.jobs.mysql_to_csv_job import MySQLToCSVJob


from writers.file_writer import FileWriter

logger = logging.getLogger(__name__)


def main():
    start_time = time.time()
    status = "SUCCESS"

    settings = Settings()

    config = settings.get_mysql_config()
    db = MySQLClient(config=config)


    try:
        db.connect()
        job = MySQLToCSVJob(
        db=db,
        file_writer=FileWriter(output_path=settings.output_path)
        )
        logger.info("Connection to MySQL was successful")

        query = "SELECT * FROM clientes"
        file_name = "clientes.csv"

        job.run(query=query, file_name=file_name)

    except Exception:
            status = "FAILED"
            logger.exception("Job Failed")

    finally:
        db.close()
        end_time = time.time()

        duration = end_time - start_time
        logger.info(f"Status: {status} | duration: {duration:.2f}s")


if __name__ == "__main__":
    main()