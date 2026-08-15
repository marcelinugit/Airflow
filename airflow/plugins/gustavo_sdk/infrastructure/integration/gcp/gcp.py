import pyarrow as pa
import pyarrow.parquet as pq
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
import google
from google.cloud import storage
from google.oauth2 import service_account
from gustavo_sdk.infrastructure.common.utils import get_logger

logger = get_logger(__name__)


class GCP:
    def __init__(
            self,
            service: google.cloud,
            credentials_file_path: Optional[str] = None,
            client: Optional[object] = None,
            credentials_json: Optional[str] = None,
            ) -> None:

        self.credentials_file_path = credentials_file_path
        self.credentials_json = credentials_json
        self.client = client or self._get_client(service)

    def _get_client(self, service: google.cloud) -> google.cloud.client:

        if self.credentials_file_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_file_path
            return service.Client()
        elif self.credentials_json:
            info = self.credentials_json

            credentials = service_account.Credentials.from_service_account_info(info=info)
            return service.Client(credentials=credentials)
        else:
            return service.Client()


    def upload_file(
        self,
        bucket_name: str,
        bucket_prefix: str,
        data: list[dict],
        file_name: str,
    ) -> None:

        with TemporaryDirectory() as root:
            file_path = Path(root) / file_name

            table = pa.Table.from_pylist(data)
            pq.write_table(table, file_path)

            bucket  = self.client.bucket(bucket_name)
            blob = bucket.blob(
                f"{bucket_prefix}/{file_name}"
            )

            blob.upload_from_filename(str(file_path))

        logger.info("File uploaded to GCP successfully")