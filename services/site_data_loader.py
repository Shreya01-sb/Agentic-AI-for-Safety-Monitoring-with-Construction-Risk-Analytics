import csv


class SiteDataLoader:
    """Loads construction site monitoring data from CSV."""

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """Read all site monitoring records from CSV."""

        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            data = []

            for row in reader:
                data.append(row)

        return data