import logging
import re
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from google.api_core.exceptions import NotFound
from google.cloud import bigquery, storage

from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP


_HIVE_PARTITION_COLUMNS = {
    "partition_year",
    "partition_month",
    "partition_day",
}


logger = logging.getLogger(__name__)


class Raw:

    def __init__(
        self,
        project_id: str,
        schema: str,
        system: str,
        table: str,
        bucket_name: str,
        year: str,
        month: str,
        day: str,
        credentials_json: dict,
    ) -> None:

        self.project_id = project_id
        self.schema = schema
        self.system = system
        self.table = table
        self.bucket_name = bucket_name
        self.year = year
        self.month = month
        self.day = day

        self.gcp_storage = GCP(
            service=storage,
            credentials_json=credentials_json,
        )

        self.gcp_bigquery = GCP(
            service=bigquery,
            credentials_json=credentials_json,
        )

    @staticmethod
    def bq_type_from_arrow(field: pa.Field) -> str:

        t = field.type

        if pa.types.is_string(t) or pa.types.is_large_string(t):
            return "STRING"

        if pa.types.is_binary(t) or pa.types.is_large_binary(t):
            return "BYTES"

        if pa.types.is_boolean(t):
            return "BOOL"

        if (
            pa.types.is_int8(t)
            or pa.types.is_int16(t)
            or pa.types.is_int32(t)
            or pa.types.is_int64(t)
            or pa.types.is_uint8(t)
            or pa.types.is_uint16(t)
            or pa.types.is_uint32(t)
            or pa.types.is_uint64(t)
        ):
            return "INT64"

        if (
            pa.types.is_float16(t)
            or pa.types.is_float32(t)
            or pa.types.is_float64(t)
        ):
            return "FLOAT64"

        if pa.types.is_decimal(t):
            return "NUMERIC"

        if pa.types.is_timestamp(t):
            return "TIMESTAMP"

        if pa.types.is_date(t):
            return "DATE"

        if pa.types.is_time(t):
            return "TIME"

        if pa.types.is_list(t) or pa.types.is_large_list(t):
            elem = t.value_field

            elem_type = Raw.bq_type_from_arrow(
                pa.field(
                    elem.name or "element",
                    elem.type,
                )
            )

            return f"ARRAY<{elem_type}>"

        if pa.types.is_struct(t):
            sub_fields = [
                f"{f.name} {Raw.bq_type_from_arrow(f)}"
                for f in t
            ]

            return f"STRUCT<{', '.join(sub_fields)}>"

        return "STRING"

    def get_parquet_schema_cols_ddl(self) -> str:

        prefix = (
            f"{self.system}/{self.table}/"
            f"partition_year={self.year}/"
            f"partition_month={self.month}/"
            f"partition_day={self.day}"
        )

        blobs = list(
            self.gcp_storage.client.list_blobs(
                self.bucket_name,
                prefix=prefix,
            )
        )

        logger.info(
            f"Blobs encontrados no prefixo {prefix}: "
            f"{[blob.name for blob in blobs]}"
        )

        parquet_blobs = [
            blob
            for blob in blobs
            if blob.name.endswith(".parquet")
        ]

        if not parquet_blobs:
            raise ValueError(
                "No .parquet files found at "
                f"gs://{self.bucket_name}/{prefix}/"
            )

        parquet_blobs.sort(
            key=lambda blob: (
                blob.time_created,
                blob.name,
            )
        )

        blob = parquet_blobs[-1]

        logger.info(
            f"Reading schema from latest parquet: {blob.name}"
        )

        with blob.open("rb") as file:
            arrow_schema = pq.ParquetFile(file).schema_arrow

        cols = [
            f"`{field.name}` "
            f"{self.bq_type_from_arrow(field)}"
            for field in arrow_schema
        ]

        return ",\n  ".join(cols)

    @staticmethod
    def schema_field_to_bq_type(
        field: bigquery.SchemaField,
    ) -> str:

        if field.field_type == "RECORD":

            sub_fields = [
                f"{sub.name} "
                f"{Raw.schema_field_to_bq_type(sub)}"
                for sub in field.fields
            ]

            base_type = (
                f"STRUCT<{', '.join(sub_fields)}>"
            )

        else:
            base_type = field.field_type

        if field.mode == "REPEATED":
            return f"ARRAY<{base_type}>"

        return base_type

    def merge_existing_table_columns(
        self,
        cols_ddl: str,
    ) -> str:

        raw_table_id = (
            f"{self.project_id}."
            f"{self.schema}."
            f"{self.table}"
        )

        try:
            existing_table = (
                self.gcp_bigquery.client.get_table(
                    raw_table_id
                )
            )

        except NotFound:
            return cols_ddl

        existing_names = set(
            re.findall(
                r"`([^`]+)`",
                cols_ddl,
            )
        )

        missing_fields = [
            field
            for field in existing_table.schema
            if (
                field.name not in existing_names
                and field.name not in _HIVE_PARTITION_COLUMNS
            )
        ]

        if not missing_fields:
            return cols_ddl

        extra_cols = ",\n  ".join(
            f"`{field.name}` "
            f"{self.schema_field_to_bq_type(field)}"
            for field in missing_fields
        )

        return f"{cols_ddl},\n  {extra_cols}"

    def build_query(
        self,
        cols_ddl: str,
    ) -> str:

        sql_path = (
            Path(__file__).resolve().parents[3]
            / "sql"
            / "pipelines"
            / "raw.sql"
        )

        with open(
            sql_path,
            "r",
            encoding="utf-8",
        ) as file:
            template = file.read()

        return template.format(
            project_id=self.project_id,
            schema=self.schema,
            table=self.table,
            cols_ddl=cols_ddl,
            bucket_name=self.bucket_name,
            system=self.system,
        )

    def execute_query(
        self,
        query: str,
    ) -> None:

        job = self.gcp_bigquery.client.query(query)
        job.result()

    def run(self) -> None:

        logger.info(
            f"Starting RAW pipeline for "
            f"{self.system}.{self.table}"
        )

        create_schema_query = (
            "CREATE SCHEMA IF NOT EXISTS "
            f"`{self.project_id}.{self.schema}`"
        )

        self.execute_query(
            create_schema_query
        )

        cols_ddl = (
            self.get_parquet_schema_cols_ddl()
        )

        cols_ddl = (
            self.merge_existing_table_columns(
                cols_ddl
            )
        )

        query = self.build_query(
            cols_ddl
        )

        logger.info(
            "Executing RAW external table query"
        )

        self.execute_query(query)

        logger.info(
            "RAW table created successfully: "
            f"{self.project_id}."
            f"{self.schema}."
            f"{self.table}"
        )