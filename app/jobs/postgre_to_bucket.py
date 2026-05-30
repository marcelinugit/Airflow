from typing import Any

from core.logger import get_logger
from integration.databases.postgres_client import PostgresClient
from writers.file_writer import FileWriter

logger = get_logger(__name__)


class PostgresToBucketJob:
    def __init__(
        self,
        db: PostgresClient,
        writer: FileWriter,
    ) -> None:
        self.db = db
        self.writer = writer

    def extract(self, query: str) -> list[dict[str, Any]]:
        if not query:
            raise ValueError("Query is required")

        logger.info("Extracting data from PostgreSQL")

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
        logger.info("Starting PostgreSQL ETL job")

        data = self.extract(query)

        if not data:
            logger.warning("No data found")
            return []

        self.load(data, file_name)

        logger.info("PostgreSQL ETL job finished successfully")

        return data