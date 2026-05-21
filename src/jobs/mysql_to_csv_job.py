import os
import csv

from src.clients.mysql_client import MySQLClient


class MySQLToCSVJob:
    def __init__(
        self,
        db: MySQLClient,
        output_path: str
    ):
        self.db = db
        self.output_path = output_path

    def get_data(self, query: str):
        return self.db.select(query)

    def save_file(
        self,
        data: list,
        file_name: str
    ):
        if not data:
            raise Exception("No data to save")

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        filepath = os.path.join(
            self.output_path,
            file_name
        )

        with open(
            filepath,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=data[0].keys()
            )

            writer.writeheader()
            writer.writerows(data)

    def run(
        self,
        query: str,
        file_name: str
    ):
        data = self.get_data(query)

        self.save_file(
            data=data,
            file_name=file_name
        )