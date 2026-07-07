from gustavo_sdk.infrastructure.common.utils import get_logger
from gustavo_sdk.infrastructure.integration.databases.mysql_client import MySQLClient
from typing import Any
from google.cloud import storage
from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP

logger = get_logger(__name__)

class MySQLToBucketJob:
    def __init__(
        self,
        db: MySQLClient,
        bucket_name: str,
        bucket_prefix: str,
        credentials_json: str,
    ) -> None:


        self.db = db
        self.bucket_name = bucket_name
        self.bucket_prefix = bucket_prefix
        self.gcp = GCP(
            service=storage,
            credentials_json=credentials_json,
        )

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

        self.gcp.upload_file(
            bucket_name=self.bucket_name,
            bucket_prefix=self.bucket_prefix,
            data=data,
            file_name=file_name,
        )

    def run(
        self,
        query: str,
        file_name: str,
    ) -> list[dict[str, Any]]:
        logger.info("Starting MySQL ETL job")

        data = self.extract(query)

        if not data:
            logger.warning("No data found in MySQL")
            return []

        self.load(data, file_name)

        logger.info("MySQL ETL job finished successfully")

        return data