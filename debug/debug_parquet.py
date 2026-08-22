import json
import pyarrow.parquet as pq
from google.cloud import storage
from google.oauth2 import service_account
import io 

SA_PATH = (
    r"C:\Users\Marce\OneDrive\Desktop\projeto dados\airflow\credentials\sa_credentials.json"
)

BUCKET_NAME = "ifood-data-lake"
FILE_PATH = (
    "ifood/usuario/"
    "partition_year=2026/"
    "partition_month=08/"
    "partition_day=15/"
    "usuario_20260815_163437.parquet"
)

with open(SA_PATH, "r") as f:
    sa_info = json.load(f)

credentials = service_account.Credentials.from_service_account_info(sa_info)
client = storage.Client(credentials=credentials)
bucket = client.bucket(BUCKET_NAME)
blob = bucket.blob(FILE_PATH)

parquet_data = blob.download_as_bytes()
table = pq.read_table(io.BytesIO(parquet_data))

type_mapping = {
    "int64": "INT64",
    "string": "STRING",
    "timestamp[us]": "TIMESTAMP",
}

columns_ddl = []
for field in table.schema:
    column_type = type_mapping[str(field.type)]
    column_ddl = f"{field.name} {column_type}"
    columns_ddl.append(column_ddl)

cols_ddl = ",\n    ".join(columns_ddl)

query = f"""
CREATE OR REPLACE EXTERNAL TABLE `ecommercegustavo-data-500420.ifood_raw.usuario`
(
    {cols_ddl}
)
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://ifood-data-lake/ifood/usuario/partition_year=2026/partition_month=08/partition_day=15/*.parquet']
)
"""