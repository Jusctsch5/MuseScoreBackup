from pathlib import Path
from hashlib import md5
import json


class MusescoreHashDatabase:
    def __init__(self, hash_database_filename):
        self.hash_database_filename = hash_database_filename

    def __get_hash_from_file(self, filename):
        bytes = 0
        with open(filename, "rb") as f:
            bytes = f.read()  # read file as bytes
            readable_hash = md5(bytes).hexdigest()
        return readable_hash

    def initialize_hash_database(self, input_dir):
        hash_database_file_exists = Path(self.hash_database_filename).is_file()

        p = Path(input_dir)
        file_paths = list(p.rglob('*.mscz'))
        hash_database = []
        for file in file_paths:
            hash_database_entry = {}
            hash = self.__get_hash_from_file(file)
            hash_database_entry['in'] = str(file)
            hash_database_entry['hash'] = hash
            hash_database.append(hash_database_entry)

        jsonString = json.dumps(hash_database, indent=4)

        with open(self.hash_database_filename, "w") as f:
            f.writelines(jsonString)
