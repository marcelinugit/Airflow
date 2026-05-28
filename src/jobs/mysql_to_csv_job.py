import logging
from src.clients.mysql_client import MySQLClient

logger = logging.getLogger(__name__)

class MySQLToCSVJob:
    def __init__(
        self,
        db: MySQLClient,
            file_writer
    ):
        self.db = db
        self.file_writer = file_writer

    def get_data(self, query: str):
        logger.info("Getting data")
        return self.db.select(query)

    def run(
        self,
        query: str,
            file_name: str
    ):
        if not query:
            raise ValueError("query is empty")

        logger.info("Running query")
        data = self.get_data(query)

        logger.info("Writing data and saving file")
        self.file_writer.save_file(data, file_name)

        logger.info("JOB was finished")
