import json
import pathlib
from typing import List


class MusescoreBatchJob:
    def __init__(self, output_file_dir_list, export_formats, content, output_dir):
        self.output_file_dir_list = output_file_dir_list
        self.export_formats = export_formats
        self.content = content

        self.filename = "batch.json"

        self.output_dir = output_dir
        self.batch_output_dir = output_dir
        self.batch_filepath = str(pathlib.Path(
            output_dir, self.filename))

    def __create_file(self):
        output_path = pathlib.Path(self.batch_output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        f = open(self.batch_filepath, "a")
        f.writelines(self.content)
        f.close()

    def process(self, musescore_interface):
        self.__create_file()

        for format in self.export_formats:
            format_output_path = pathlib.Path(self.output_dir,
                                              format)
            print("Creating output format directory:" + str(format_output_path))
            try:
                format_output_path.mkdir(parents=True, exist_ok=True)
            except:
                print("Error attempting to create path:" +
                      str(format_output_path))
                exit(1)

            for output_file_dir in self.output_file_dir_list:
                output_file_dir_path = pathlib.Path(self.output_dir,
                                                    format, output_file_dir)
                print("Creating output file directory:" +
                      str(output_file_dir_path))
                try:
                    output_file_dir_path.mkdir(parents=True, exist_ok=True)
                except:
                    print("Error attempting to create path:" +
                          str(output_file_dir_path))
                    exit(1)

        musescore_interface.process_batch(self)


class MusescoreBatchJobCreator:

    def create_batch_from_file_list(self, files: List[str], input_dir: str, output_dir: str, export_formats) -> MusescoreBatchJob:

        if len(files) == 0:
            print("Input files length of 0")
            return None

        p = pathlib.Path(input_dir)

        batch_job_json = []
        output_file_dir_list = []
        for filename in files:
            batch = {}

            batch['in'] = filename

            output_filepath = pathlib.Path(filename).relative_to(p)
            output_file_dir_list.append(output_filepath.parent)

            batch['out'] = []

            for format in export_formats:
                output_format = str(pathlib.Path(
                    output_dir, format, str(output_filepath.with_suffix("")) + "." + format))
                batch['out'].append(output_format)

            batch_job_json.append(batch)

        jsonString = json.dumps(batch_job_json, indent=4)
        job = MusescoreBatchJob(output_file_dir_list,
                                export_formats, jsonString, output_dir)
        return job

    def create_batch_from_directory(self, input_dir, output_dir, export_formats):

        print("Scanning directory for file_paths: " + input_dir)
        p = pathlib.Path(input_dir)
        file_paths = list(str(p.rglob('*.mscz')))

        return self.create_batch_from_file_list(file_paths, input_dir, output_dir, export_formats)

    def create_batch_from_hash_database(self, hash_db, input_dir, output_dir, export_formats):
        file_paths = hash_db.get_hash_diff_list()

        return self.create_batch_from_file_list(file_paths, input_dir, output_dir, export_formats)
