from gustavo_sdk.infrastructure.common.utils import get_logger
from google.cloud import storage
from tempfile import TemporaryDirectory
import csv
from pathlib import Path

logger = get_logger(__name__)

class GCP:
    def __init__(self) -> None:
        self.client = storage.Client()

    def upload(
            self,
            bucket_prefix: str,
            data: list[dict],
            file_name: str,
            ) -> None:

        with TemporaryDirectory() as root:
            file_path = Path(root) / file_name
            print(file_path)

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            bucket = self.client.bucket(bucket_prefix)
            blob = bucket.blob(file_name)
            blob.upload_from_filename(str(file_path))

        logger.info("File uploaded to GCP successfully")