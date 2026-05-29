import os
import csv
from typing import List, Dict
from core.logger import get_logger

logger = get_logger(__name__)


class FileWriter:
    def __init__(self, output_path: str) -> None:
        self.output_path = output_path

    def save_file(self, data: List[Dict], file_name: str) -> None:
        if not data:
            raise ValueError("No data to write")

        os.makedirs(self.output_path, exist_ok=True)

        file_path = os.path.join(self.output_path, file_name)

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"File saved at {file_path}")