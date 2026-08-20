import json
from datetime import datetime

from gustavo_sdk.app.airflow_functions import mysql_to_bucket

SA_PATH = (
    r"C:\Users\Marce\OneDrive\Desktop\projeto dados\airflow\credentials\sa_credentials.json"
)

with open(SA_PATH, "r") as f:
    sa_info = json.load(f)

today = datetime.now()

hive_partition = (
    f"partition_year={today.year}/"
    f"partition_month={today.month:02d}/"
    f"partition_day={today.day:02d}"
)

timestamp = today.strftime("%Y%m%d_%H%M%S")

parameters = {
    "host": "localhost",
    "user": "admin",
    "password": "123456",
    "port": "3306",
    "database": "airflow_db",
    "table_name": "usuario",
    "file_name": f"usuario_{timestamp}.csv",
    "bucket_name": "mercadolivre-data-lake",
    "bucket_prefix": f"mercadolivre/usuario/{hive_partition}",
    "credentials_json": sa_info,
}

mysql_to_bucket(**parameters)

print("MySQL debug finished successfully!")