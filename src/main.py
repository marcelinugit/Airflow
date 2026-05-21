from src.config.settings import Settings
from src.clients.mysql_client import MySQLClient
from src.jobs.mysql_to_csv_job import MySQLToCSVJob


settings = Settings()

config = settings.get_mysql_config()

db = MySQLClient(config=config)

db.connect()

job = MySQLToCSVJob(
    db=db,
    output_path=settings.output_path
)

query = "SELECT * FROM clientes"

job.run(
    query=query,
    file_name="clientes.csv"
)

db.close()