from src.clients.mysql_client import MySQLClient
from src.config.settings import Settings

def test_connection():
    settings = Settings()
    client = MySQLClient(settings.get_mysql_config())

    client.connect()

    assert client.conn is not None
    assert client.cursor is not None

    client.close()