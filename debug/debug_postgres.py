import json
from datetime import datetime

from gustavo_sdk.app.airflow_functions import postgres_to_bucket

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
    "port": "5432",
    "database": "airflow_db",
    "table_name": "usuario",
    "file_name": f"usuario_{timestamp}.parquet",
    "bucket_name": "ifood-data-lake",
    "bucket_prefix": f"ifood/usuario/{hive_partition}",
    "credentials_json": sa_info,
}

postgres_to_bucket(**parameters)

print("PostgreSQL debug finished successfully!")