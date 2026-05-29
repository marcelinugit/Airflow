from typing import Any

from core.logger import get_logger
from integration.databases.mysql_client import MySQLClient
from writers.file_writer import FileWriter

logger = get_logger(__name__)


class MySQLToBucketJob:
    def __init__(
        self,
        db: MySQLClient,
        writer: FileWriter,
    ) -> None:
        self.db = db
        self.writer = writer

    def extract(self, query: str) -> list[dict[str, Any]]:
        if not query:
            raise ValueError("Query is required")

        logger.info("Extracting data from MySQL")
        return self.db.select(query)

    def load(
        self,
        data: list[dict[str, Any]],
        file_name: str,
    ) -> None:
        self.writer.save_file(data, file_name)

    def run(
        self,
        query: str,
        file_name: str,
    ) -> list[dict[str, Any]]:
        logger.info("Starting ETL job")

        data = self.extract(query)

        if not data:
            logger.warning("No data found")
            return []

        self.load(data, file_name)

        logger.info("ETL job finished successfully")

        return data