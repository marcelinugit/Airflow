import csv
import logging
import os
from typing import Any
from gustavo_sdk.infrastructure.integration.gcp.gcp import GCP

def get_logger(name: str) -> logging.Logger:
    app_logger = logging.getLogger(name)

    if not app_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        app_logger.addHandler(handler)
        app_logger.setLevel(logging.INFO)

    return app_logger


logger = get_logger(__name__)


def save_file(
    output_path: str,
    data: list[dict[str, Any]],
    file_name: str,
) -> None:

    if not data:
        raise ValueError("No data to write")

    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, file_name)

    logger.info(f"Writing file: {file_path}")

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

    logger.info(f"File saved at: {os.path.abspath(file_path)}")