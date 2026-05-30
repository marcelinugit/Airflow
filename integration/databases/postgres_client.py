from typing import Any
import psycopg2

from core.logger import get_logger

logger = get_logger(__name__)


class PostgresClient:
    def __init__(self, config: dict[str, str]) -> None:
        self.config = config
        self.conn = None

    def connect(self) -> Any:
        try:
            self.conn = psycopg2.connect(
                host=self.config["host"],
                database=self.config["database"],
                user=self.config["user"],
                password=self.config["password"],
                port=self.config["port"],
            )

            logger.info("Connected to PostgreSQL")

            return self.conn

        except psycopg2.Error as error:
            logger.error(f"Connection failed: {error}")
            raise

    def close(self) -> None:
        if self.conn:
            logger.info("Closing PostgreSQL connection")
            self.conn.close()

    def select(self, query: str) -> list[dict[str, Any]]:
        if self.conn is None:
            raise ConnectionError("Database is not connected")

        logger.info("Executing SELECT query")

        with self.conn.cursor() as cursor:
            cursor.execute(query)

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]