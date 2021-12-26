from .configuration_decoder import ConfigurationDecoder
from .musescore_hash_database import MusescoreHashDatabase

import pathlib


def test_musescore_hash_database():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        str(pathlib.Path("musescore_backup_module", "test", "test_hash_config.json")))

    database = MusescoreHashDatabase(
        configuration.decoded_object.VersionDatabase)
    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)
