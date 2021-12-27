from pathlib import Path
from hashlib import md5
import json
from jsondiff import diff


class MusescoreHashDatabase:
    def __init__(self, hash_database_filename):
        self.hash_database_filename = hash_database_filename
        self.previous_hash_content = ""
        self.current_hash_content = ""

    def __get_hash_from_file(self, filename):
        bytes = 0
        with open(filename, "rb") as f:
            bytes = f.read()  # read file as bytes
            readable_hash = md5(bytes).hexdigest()
        return readable_hash

    def __retrieve_hash_content(self, input_dir):
        p = Path(input_dir)
        file_paths = list(p.rglob('*.mscz'))
        hash_database = []
        for file in file_paths:
            hash_database_entry = {}
            hash = self.__get_hash_from_file(file)
            hash_database_entry['in'] = str(file)
            hash_database_entry['hash'] = hash
            hash_database.append(hash_database_entry)

        return json.dumps(hash_database, indent=4)

    def clear_hash_database(self):
        file_to_rem = Path(self.hash_database_filename)
        file_to_rem.unlink()

    def initialize_hash_database(self, input_dir):

        self.current_hash_content = content = self.__retrieve_hash_content(
            input_dir)

        hash_database_file_exists = Path(self.hash_database_filename).is_file()
        if hash_database_file_exists is False:
            with open(self.hash_database_filename, "w") as f:
                f.writelines(content)
        else:
            with open(self.hash_database_filename, "r") as f:
                content = json.loads(f.read())

        self.previous_hash_content = content

    def get_hash_diff_list(self):
        # Get the entries in the "current" hash content that are either
        # 1) not the same
        # 2) not present
        # in the "previous" hash
