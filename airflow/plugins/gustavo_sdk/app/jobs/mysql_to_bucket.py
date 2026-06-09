from typing import Any

from gustavo_sdk.infrastructure.common.config.settings import Settings
from gustavo_sdk.infrastructure.common.utils import get_logger, save_file
from gustavo_sdk.infrastructure.integration.databases.mysql_client import MySQLClient

logger = get_logger(__name__)


class MySQLToBucketJob:
    def __init__(
        self,
        db: MySQLClient,
    ) -> None:
        self.db = db
        self.settings = Settings()

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

        save_file(
            output_path=self.settings.output_path or "data/landing",
            data=data,
            file_name=file_name
        )

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
