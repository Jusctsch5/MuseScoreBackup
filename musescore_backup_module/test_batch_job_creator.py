from musescore_backup_module.musescore_hash_database import MusescoreHashDatabase
from .configuration_decoder import ConfigurationDecoder
from .musescore_batch_job_creator import MusescoreBatchJobCreator
from .musescore_interface import MusescoreReal

import pathlib


def test_batch_job():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("musescore_backup_module", "test", "test1", "test_config.json"))

    creator = MusescoreBatchJobCreator()

    batch_job = creator.create_batch_from_directory(configuration.decoded_object.InputDirectory,
                                                    configuration.decoded_object.OutputDirectory,
                                                    ["mp3"])

    interface = MusescoreReal(
        configuration.decoded_object.MuseScoreInstallDirectory)

    batch_job.process(interface)


def test_batch_job_hash():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("musescore_backup_module", "test", "test1", "test_hash_config.json"))

    database = MusescoreHashDatabase(
        configuration.decoded_object.HashDatabase)

    database.clear_hash_database()

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    creator = MusescoreBatchJobCreator()

    batch_job = creator.create_batch_from_hash_database(database,
                                                        configuration.decoded_object.InputDirectory,
                                                        configuration.decoded_object.OutputDirectory,
                                                        ["mp3"])
    interface = MusescoreReal(
        configuration.decoded_object.MuseScoreInstallDirectory)

    print("previous:" + str(database.previous_hash_content))
    print("current:" + str(database.current_hash_content))

    batch_job.process(interface)
