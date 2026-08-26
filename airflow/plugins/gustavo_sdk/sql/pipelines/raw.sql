CREATE OR REPLACE EXTERNAL TABLE
`{project_id}.{schema}.{table}`
(
    {cols_ddl}
)
WITH PARTITION COLUMNS
(
    partition_year INT64,
    partition_month INT64,
    partition_day INT64
)
OPTIONS (
    format = 'PARQUET',
    uris = [
        'gs://{bucket_name}/{system}/{table}/*.parquet'
    ],
    hive_partition_uri_prefix =
        'gs://{bucket_name}/{system}/{table}/'
);