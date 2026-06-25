import csv
from pathlib import Path
from tempfile import TemporaryDirectory
from airflow.hooks.base import BaseHook
from google.cloud import storage
from google.oauth2 import service_account
from gustavo_sdk.infrastructure.common.utils import get_logger
import json

logger = get_logger(__name__)


class GCP:
    def __init__(self):
        conn = BaseHook.get_connection("gcp_default")

        service_account_info = json.loads(
            conn.extra_dejson["keyfile_dict"]
        )

        credentials = service_account.Credentials.from_service_account_info(
                    service_account_info
        )

        self.client = storage.Client(
            credentials=credentials,
            project=conn.extra_dejson["project"],
        )

    def upload(
        self,
        bucket_name: str,
        bucket_prefix: str,
        data: list[dict],
        file_name: str,
    ) -> None:

        with TemporaryDirectory() as root:
            file_path = Path(root) / file_name

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(f"{bucket_prefix}/{file_name}")
            blob.upload_from_filename(str(file_path))

        logger.info("File uploaded to GCP successfully")