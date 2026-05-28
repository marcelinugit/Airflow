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

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            return data


    def insert(self, query: str, values: tuple):
        if not query:
            raise ValueError("Query is required")

        if not values:
            raise ValueError("Values are required")

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            self.conn.commit()

            logger.info("Inserted into MySQL")

    def update(self, query: str, values: tuple):
        if not query:
            raise ValueError("Query is required")

        if not values:
            raise ValueError("Values are required")

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            self.conn.commit()

            logger.info("Updated MySQL")

    def delete(self, query: str, values: tuple):
        if not query:
            raise ValueError("Query is required")

        if not values:
            raise ValueError("Values are required")

        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            self.conn.commit()

            logger.info("Deleted from MySQL")