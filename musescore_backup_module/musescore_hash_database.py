from pathlib import Path
from hashlib import md5
import json


class MusescoreHashDatabase:
    def __init__(self, hash_database_filename):
        self.hash_database_filename = hash_database_filename
        self.previous_hash_content = []
        self.current_hash_content = []

    def __get_hash_from_file(self, filename):
        bytes = 0
        with open(filename, "rb") as f:
            bytes = f.read()  # read file as bytes
            readable_hash = md5(bytes).hexdigest()
        return readable_hash

    def __retrieve_hash_content(self, input_dir):
        print("Retrieving hash content from: " + input_dir)
        p = Path(input_dir)
        file_paths = list(p.rglob('*.mscz'))
        hash_database = []
        for file in file_paths:
            hash_database_entry = {}
            hash = self.__get_hash_from_file(file)
            hash_database_entry['in'] = str(file)
            hash_database_entry['hash'] = hash
            hash_database.append(hash_database_entry)

        return hash_database

    def clear_hash_database(self):
        file_to_rem = Path(self.hash_database_filename)
        if file_to_rem.is_file() is False:
            return
        file_to_rem.unlink()

    def initialize_hash_database(self, input_dir):

        self.current_hash_content = content = self.__retrieve_hash_content(
            input_dir)

        hash_database_file_exists = Path(self.hash_database_filename).is_file()
        if hash_database_file_exists is False:
            pass
        else:
            with open(self.hash_database_filename, "r") as f:
                content = json.loads(f.read())
            self.previous_hash_content = content

    def update_hash_database(self):
        with open(self.hash_database_filename, "w") as f:
            f.writelines(json.dumps(self.current_hash_content, indent=4))

    def get_hash_diff_list(self):
        # Get the entries in the "current" hash content that are either
        # 1) not the same
        # 2) not present
        # in the "previous" hash

        hash_diff_list = []
        for current_in in self.current_hash_content:
            match = False
            if len(self.previous_hash_content) > 0:
                for previous_in in self.previous_hash_content:
                    if current_in['in'] == previous_in['in'] and \
                            current_in['hash'] == previous_in['hash']:
                        match = True
                        continue

            if match is False:
                hash_diff_list.append(current_in['in'])

        return hash_diff_list
