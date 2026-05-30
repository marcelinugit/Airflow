import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        # MySQL
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")

        # PostgreSQL
        self.postgres_host = os.getenv("POSTGRES_HOST")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_database = os.getenv("POSTGRES_DATABASE")
        self.postgres_port = os.getenv("POSTGRES_PORT")

        # Output
        self.output_path = os.getenv("OUTPUT_PATH")

    def _validate(
        self,
        config: dict[str, str | None]
    ) -> dict[str, str]:
        """
        Validate environment variables before returning config.
        """

        missing_vars = [
            key
            for key, value in config.items()
            if value is None
        ]

        if missing_vars:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing_vars)}"
            )

        return {
            key: value
            for key, value in config.items()
            if value is not None
        }

    def get_mysql_config(self) -> dict[str, str]:
        return self._validate(
            {
                "host": self.mysql_host,
                "user": self.mysql_user,
                "password": self.mysql_password,
                "database": self.mysql_database,
            }
        )

    def get_postgres_config(self) -> dict[str, str]:
        return self._validate(
            {
                "host": self.postgres_host,
                "user": self.postgres_user,
                "password": self.postgres_password,
                "database": self.postgres_database,
                "port": self.postgres_port,
            }
        )