from typing import List, Dict
from core.logger import get_logger

logger = get_logger(__name__)


class MySQLToBucketJob:
    def __init__(self, db, writer) -> None:
        self.db = db
        self.writer = writer

    def extract(self, query: str) -> List[Dict]:
        if not query:
            raise ValueError("Query is required")

        logger.info("Extracting data from MySQL")
        return self.db.select(query)

    def run(self, query: str, file_name: str) -> List[Dict]:
        logger.info("Starting ETL job")

        data = self.extract(query)

        if not data:
            logger.warning("No data found")
            return []

        self.writer.save_file(data, file_name)

        logger.info("ETL job finished successfully")

        return data