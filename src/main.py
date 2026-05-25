from src.config.settings import Settings
from src.clients.mysql_client import MySQLClient
from src.jobs.mysql_to_csv_job import MySQLToCSVJob
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    settings = Settings()

    config = settings.get_mysql_config()

    db = MySQLClient(config=config)

    try:
        db.connect()

        job = MySQLToCSVJob(
            db=db,
            output_path=settings.output_path
        )

        query = "SELECT * FROM clientes"

        job.run(
            query=query,
            file_name="clientes.csv"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()