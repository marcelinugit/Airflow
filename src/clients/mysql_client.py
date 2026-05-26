import mysql.connector
import logging

logger = logging.getLogger(__name__)

class MySQLClient:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None

    def connect(self):
        logger.info("Connecting to MySQL")


        self.conn = mysql.connector.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
        )
        logger.info("Connected to MySQL")
        return self.conn

    def close(self):

        if self.conn:
            self.conn.close()

    def select(self, query: str):
        if not query:
            raise ValueError("Query is required")

        logger.info(f"Executing query: {query}")

        with self.conn.cursor(dictionary=True) as cursor:

            cursor.execute(query)
            logger.info("Query executed")

            data = cursor.fetchall()
            logger.info("data fatched")

            return data
