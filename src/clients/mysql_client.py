import mysql.connector
import logging


class MySQLClient:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        logging.info("Connecting to MySQL")


        self.conn = mysql.connector.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
        )
        logging.info("Connected to MySQL")

        self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

    def select(self, query: str):
        if not query:
            raise Exception("Query is required")

        if not self.cursor:
            raise Exception("Connection is not initialized")

        try:
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query)

            dados = self.cursor.fetchall()
            logging.info(f"Fetched {len(dados)} rows")

            colunas = [
                desc[0]
                for desc in self.cursor.description
            ]

            result = []

            for linha in dados:
                result.append(
                    dict(zip(colunas, linha))
                )

            return result

        except mysql.connector.Error as error:
            raise Exception(
                f"MySQL error while executing query: {query}"
            ) from error