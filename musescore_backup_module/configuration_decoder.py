from types import SimpleNamespace
import json


class Configuration:

    """
     Configuration - Decodes configuration information
    """

    def __init__(self, i_decoded_object):
        self.decoded_object = i_decoded_object


class ConfigurationDecoder:

    """
     ConfigurationDecoder - Decodes input json Configuration file and creates a Configuration class
    """

    def __init__(self):
        pass

    def __decode_configuration(self, configuration_filepath):
        with configuration_filepath.open() as f:
            x = json.load(f, object_hook=lambda d: SimpleNamespace(**d))

        configuration = Configuration(x)
        return configuration

    def decode_configuration(self, configuration_filepath):
        return self.__decode_configuration(configuration_filepath)
