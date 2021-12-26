import json
import pathlib
import datetime
import uuid


class MusescoreBatchJob:
    def __init__(self, export_formats, content, output_dir, batch_file_dir):
        self.export_formats = export_formats
        self.content = content

        now = datetime.datetime.now()

        self.filename = "Batch_" + \
            str(now.year) + "_" + \
            str(now.month) + "_" + \
            str(now.day) + "_" + \
            str(uuid.uuid4())[0:8] + \
            ".json"

        self.output_dir = output_dir
        self.batch_output_dir = batch_file_dir
        self.batch_filepath = str(pathlib.Path(
            batch_file_dir, self.filename))

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
            print("Creating output directory:" + str(format_output_path))

            try:
                format_output_path.mkdir(parents=True, exist_ok=True)
            except:
                print("Error attempting to create path:" +
                      str(format_output_path))
                exit(1)

        musescore_interface.process_batch(self)


class MusescoreBatchJobCreator:

    def create_batch_from_directory(self, input_dir, output_dir, export_formats):

        batch_job_json = []
        print("Scanning directory for file_paths: " + input_dir)
        p = pathlib.Path(input_dir)
        file_paths = list(p.rglob('*.mscz'))

        for file_path in file_paths:
            batch = {}

            batch['in'] = str(file_path)

            output_filepath = file_path.relative_to(p)
            batch['out'] = []

            for format in export_formats:
                output_format = str(pathlib.Path(
                    output_dir, "output", format, str(output_filepath.with_suffix("")) + "." + format))
                batch['out'].append(output_format)

            batch_job_json.append(batch)

        jsonString = json.dumps(batch_job_json, indent=True)
        job = MusescoreBatchJob(
            export_formats, jsonString, output_dir, "batch_jobs")

        return job
