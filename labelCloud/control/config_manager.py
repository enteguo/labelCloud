"""Load configuration from .ini file."""
import configparser

# Read local file `config.ini`.
import os
from typing import List, Union, Optional


class ExtendedConfigParser(configparser.ConfigParser):

    def getlist(self, section, option, raw=False, vars=None, fallback=None) -> List:
        raw_value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        if "," in raw_value:
            values = [x.strip() for x in raw_value.split(',')]
            try:
                return [float(item) for item in values]
            except ValueError:
                return values
        return raw_value


class ConfigManager(object):
    PATH_TO_CONFIG = "config.ini"
    PATH_TO_DEFAULT_CONFIG = "ressources/default_config.ini"

    def __init__(self):
        self.config = ExtendedConfigParser(comment_prefixes='/', allow_no_value=True)
        self.read_from_file()

    def read_from_file(self):
        if os.path.isfile(ConfigManager.PATH_TO_CONFIG):
            self.config.read(ConfigManager.PATH_TO_CONFIG)
        else:
            self.config.read(ConfigManager.PATH_TO_DEFAULT_CONFIG)

    def write_into_file(self):
        with open(ConfigManager.PATH_TO_CONFIG, 'w') as configfile:
            self.config.write(configfile, space_around_delimiters=True)

    def reset_to_default(self):
        self.config.read(ConfigManager.PATH_TO_DEFAULT_CONFIG)

    def get_file_settings(self, key: str) -> str:
        return self.config["FILE"][key]


config_manager = ConfigManager()
config = config_manager.config
