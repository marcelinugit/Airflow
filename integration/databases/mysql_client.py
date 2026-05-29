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

    def select(self, query: str) -> list[dict]:
        if not self.conn:
            raise ConnectionError("Database not connected")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()