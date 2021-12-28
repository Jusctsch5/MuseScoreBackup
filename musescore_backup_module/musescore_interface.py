from abc import ABC, abstractmethod
import subprocess
from datetime import datetime
import pathlib


class MusescoreInterface(ABC):
    @abstractmethod
    def process_batch(self, batch_job):
        pass


class MusescoreFake(MusescoreInterface):
    def __init__(self):
        pass

    def process_batch(self, batch_job):
        for file in batch_job:
            for output in file['out']:
                pathlib.Path(output).touch()


class MusescoreReal(MusescoreInterface):

    def __init__(self, musescore_binary):
        self.musescore_binary = musescore_binary

    def process_batch(self, batch_job):
        print("Running MuseScore Command on batch file:{}".format(batch_job.filename))
        then = datetime.now()
        response = subprocess.run(
            [self.musescore_binary, "-j", batch_job.batch_filepath], stdout=subprocess.PIPE, text=True, input="Hello from the other side")
        print(response)

        now = datetime.now()
        print("Time Elapsed:" + str(now - then))
