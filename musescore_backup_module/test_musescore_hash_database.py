from .configuration_decoder import ConfigurationDecoder
from .musescore_hash_database import MusescoreHashDatabase

import pathlib


def test_musescore_hash_database():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("musescore_backup_module", "test", "test1", "test_hash_config.json"))

    database = MusescoreHashDatabase(
        configuration.decoded_object.HashDatabase)

    database.clear_hash_database()

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    assert(database.previous_hash_content == database.current_hash_content)

    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("musescore_backup_module", "test", "test2", "test_hash_config.json"))

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    print(database.previous_hash_content)
    print(database.current_hash_content)

    assert(database.previous_hash_content != database.current_hash_content)
    print("previous:" + str(database.previous_hash_content))
    print("current:" + str(database.current_hash_content))
    print("diff:" + str(database.get_hash_diff_list()))
