import os
import csv
import logging

logger = logging.getLogger(__name__)

class FileWriter:
    def __init__(self, output_path):
        self.output_path = output_path

    def save_file(self, data: list, file_name: str):

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        if not data:
            raise ValueError("Data is required")

        new_file = os.path.join(self.output_path, file_name)
        logger.info("Saving data to file")

        with open(new_file, "w",newline="",
                  encoding="utf-8") as file :
            writer = csv.DictWriter(file,
                                    fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
            logger.info("file created successfully")