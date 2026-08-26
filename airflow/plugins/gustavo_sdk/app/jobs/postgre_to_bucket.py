from google.cloud import storage
from gustavo_sdk.infrastructure.common.utils import get_logger
from gustavo_sdk.infrastructure.integration.databases.postgres_client import PostgresClient
from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP

logger = get_logger(__name__)


class PostgresToBucketJob:
    def __init__(
            self,
            db: PostgresClient,
            bucket_name: str,
            bucket_prefix: str,
            credentials_json: str,
    ) -> None:

        self.db = db
        self.bucket_name = bucket_name
        self.bucket_prefix = bucket_prefix
        self.gcp = GCP(
            service=storage,
            credentials_json=credentials_json,
        )


    def run(
            self,
            query: str,
            batch_size: int = 10_000,
    ) -> None:

        logger.info(
            f"Starting PostgreSQL ETL job with batch_size={batch_size}"
        )

        cursor = self.db.select(query)

        total_rows = 0
        batch_number = 0

        try:
            columns = [desc[0] for desc in cursor.description]

            while True:
                rows = cursor.fetchmany(batch_size)

                if not rows:
                    break

                batch_number += 1

                data = [
                    dict(zip(columns, row))
                    for row in rows
                ]

                self.gcp.upload_parquet_file(
                    bucket_name=self.bucket_name,
                    bucket_prefix=self.bucket_prefix,
                    data=data,
                )

                total_rows += len(data)

                logger.info(
                    f"Batch {batch_number} uploaded: "
                    f"{len(data)} rows | "
                    f"total={total_rows}"
                )

        finally:
            cursor.close()

        if total_rows == 0:
            logger.warning("No data found in PostgreSQL")
            return

        logger.info(
            f"PostgreSQL ETL job finished successfully. "
            f"Total rows: {total_rows}"
        )