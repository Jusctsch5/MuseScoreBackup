from .configuration_decoder import ConfigurationDecoder
from .musescore_batch_job_creator import MusescoreBatchJobCreator
from .musescore_interface import MusescoreInterface

import unittest
import pathlib


def test_batch_job():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        str(pathlib.Path("musescore_backup_module", "test", "test_config.json")))

    creator = MusescoreBatchJobCreator()

    batch_job = creator.create_batch_from_directory(configuration.decoded_object.InputDirectory,
                                                    configuration.decoded_object.OutputDirectory,
                                                    ["mp3"])

    interface = MusescoreInterface(
        configuration.decoded_object.MuseScoreInstallDirectory)

    batch_job.process(interface)
