import csv


class SafetyDataLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Load worker safety data from CSV."""

        with open(
            self.file_path,
            mode="r",
            newline="",
            encoding="utf-8"
        ) as file:

            return list(csv.DictReader(file))