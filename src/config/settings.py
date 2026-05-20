import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")
        self.output_path = os.getenv("OUTPUT_PATH")

    def get_mysql_config(self):
        return {
            "host": self.mysql_host,
            "user": self.mysql_user,
            "password": self.mysql_password,
            "database": self.mysql_database,
        }