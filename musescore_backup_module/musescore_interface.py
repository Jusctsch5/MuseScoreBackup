import subprocess
from datetime import datetime


class MusescoreInterface:

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
