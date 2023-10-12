import csv
import os.path
from datetime import datetime

class CSVSaver:

    def __init__(self, csv_file_path: str):
        self.file_path = csv_file_path
        self.fieldnames = ['name', 'email', 'message']
        self.data: list = self.load()

    def load(self) -> list:
        mode = 'r'

        if not os.path.exists(self.file_path):
            mode = 'w'

        with open(self.file_path, mode, encoding='utf-8') as csv_in:
            reader = csv.DictReader(csv_in, delimiter=';', fieldnames=self.fieldnames)
            return list(reader)

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as csv_out:
            writer = csv.DictWriter(csv_out, delimiter=';', fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.data)


class UserMessagesSaver(CSVSaver):

    def __init__(self, csv_file_path: str):
        super().__init__(csv_file_path)
        self.fieldnames = ['name', 'email', 'message', 'timestamp']

    def save_message(self, post_data: dict):
        data = {
            'name': post_data['name'],
            'email': post_data['email'],
            'message': post_data['message'],
            'timestamp': datetime.utcnow()
        }

        self.data.append(data)
        self.save()


messages_saver = UserMessagesSaver(os.path.join('catalog', 'files', 'user_messages.csv'))



