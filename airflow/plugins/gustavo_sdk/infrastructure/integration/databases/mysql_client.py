from typing import Any, Dict, List, Optional
import mysql.connector

# Corrigido o import apontando para a pasta comum de utils
from gustavo_sdk.infrastructure.common.utils import get_logger

logger = get_logger(__name__)


class MySQLClient:
    def __init__(self, config: Dict[str, str]) -> None:
        self.config = config
        self.conn: Optional[Any] = None

    def connect(self) -> Any:
        logger.info("Connecting to MySQL")

        self.conn = mysql.connector.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
        )

        logger.info("Connected to MySQL")
        return self.conn

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            logger.info("Connection closed")

    def select(self, query: str) -> List[Dict]:
        if not self.conn:
            raise ConnectionError("Database not connected")

        with self.conn.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            return cursor.fetchall()
