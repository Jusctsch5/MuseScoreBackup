from musescore_backup_module.configuration_decoder import ConfigurationDecoder
from musescore_backup_module.musescore_hash_database import MusescoreHashDatabase

import pathlib


def test_musescore_hash_database():
    configuration_decoder = ConfigurationDecoder()
    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("test_musescore_backup_module", "test1", "test_hash_config.json"))

    database = MusescoreHashDatabase(
        configuration.decoded_object.HashDatabase)

    database.clear_hash_database()

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    assert(database.previous_hash_content != database.current_hash_content)

    # Simulate generation of files, which should update the cache
    # then relaunch and verify nothing needs to be generated
    database.update_hash_database()
    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)
    assert(database.previous_hash_content == database.current_hash_content)

    # Cache is updated
    # now add a new file, and make sure it needs to be modified
    configuration = configuration_decoder.decode_configuration(
        pathlib.Path("test_musescore_backup_module", "test2", "test_hash_config.json"))

    database.initialize_hash_database(
        configuration.decoded_object.InputDirectory)

    print(database.previous_hash_content)
    print(database.current_hash_content)

    assert(database.previous_hash_content != database.current_hash_content)
    print("previous:" + str(database.previous_hash_content))
    print("current:" + str(database.current_hash_content))
    print("diff:" + str(database.get_hash_diff_list()))
