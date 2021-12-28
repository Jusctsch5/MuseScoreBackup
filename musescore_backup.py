#!/usr/bin/env python
import argparse
from musescore_backup_module.configuration_decoder import ConfigurationDecoder
from musescore_backup_module.musescore_hash_database import MusescoreHashDatabase
from musescore_backup_module.musescore_interface import MusescoreReal
from musescore_backup_module.musescore_batch_job_creator import MusescoreBatchJobCreator
from pathlib import Path

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Perform a musescore backup operation.')
    parser.add_argument("-i", '--input', help="")
    parser.add_argument("-o", '--output', help="")
    parser.add_argument('-c', '--configuration',
                        required=True, help='Configuration file')
    args = parser.parse_args()

    print("Launching Musescore Backup with arguments: " + str(args))

    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        Path(args.configuration))

    database = MusescoreHashDatabase(
        configuration.decoded_object.HashDatabase)

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    creator = MusescoreBatchJobCreator(database)

    batch_job = creator.create_batch_from_directory(configuration.decoded_object.InputDirectory,
                                                    configuration.decoded_object.OutputDirectory,
                                                    configuration.decoded_object.ExportFormats)

    interface = MusescoreReal(
        configuration.decoded_object.MuseScoreInstallDirectory)
    batch_job.process(interface)
