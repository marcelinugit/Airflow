from typing import Any
import csv
import os

from core.logger import get_logger

logger = get_logger(__name__)


class FileWriter:
    def __init__(self, output_path: str) -> None:
        self.output_path = output_path

    def save_file(
        self,
        data: list[dict[str, Any]],
        file_name: str,
    ) -> None:

        if not data:
            raise ValueError("No data to write")

        os.makedirs(
            self.output_path,
            exist_ok=True,
        )

        file_path = os.path.join(
            self.output_path,
            file_name,
        )

        logger.info(
            f"Writing file: {file_path}"
        )

        with open(
            file_path,
            mode="w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=data[0].keys(),
            )

            writer.writeheader()
            writer.writerows(data)

        logger.info(
            f"File saved at: {os.path.abspath(file_path)}"
        )