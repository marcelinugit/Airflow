import logging
from pathlib import Path
from google.cloud import bigquery

from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP


logger = logging.getLogger(__name__)


class Bronze:

    def __init__(
        self,
        project_id: str,
        system: str,
        table: str,
        pk: str,
        credentials_json: dict,
    ) -> None:

        self.project_id = project_id
        self.system = system
        self.table = table
        self.pk = pk

        self.gcp_bigquery = GCP(
            service=bigquery,
            credentials_json=credentials_json,
        )

    def build_query(self) -> str:

        sql_path = (
            Path(__file__).resolve().parents[3]
            / "sql"
            / "pipelines"
            / "bronze_most_recent.sql"
        )

        with open(
            sql_path,
            "r",
            encoding="utf-8",
        ) as file:
            template = file.read()

        return template.format(
            project_id=self.project_id,
            system=self.system,
            table=self.table,
            pk=self.pk,
        )

    def execute_query(
        self,
        query: str,
    ) -> None:

        job = self.gcp_bigquery.client.query(query)
        job.result()

    def run(self) -> None:

        logger.info(
            f"Starting BRONZE pipeline for "
            f"{self.system}.{self.table}"
        )

        query = self.build_query()

        logger.info(
            "Executing BRONZE most recent query"
        )

        self.execute_query(query)

        logger.info(
            "BRONZE table created successfully: "
            f"{self.project_id}."
            f"{self.system}_bronze."
            f"{self.table}"
        )