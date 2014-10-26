import json
import os

from pinger.exceptions import ConfigException


class Config(object):
    """
    Config handler object.
    """
    config = None

    def __init__(self, config_file):
        self.config = self._set_config(config_file)

    def __repr__(self):
        return str(self.config)

    def _set_config(self, config_file):
        if not os.path.exists(config_file):
            raise ConfigException('Could not find config file.')

        with open(config_file, 'r') as f_:
            try:
                return json.loads(f_.read())
            except ValueError:
                raise ConfigException('Could not decode config file.')

    def __getitem__(self, key):
        if not self.config:
            raise ConfigException('Config not loaded')

        return self.config[key]

    def get(self, key, replacement):
        try:
            return self.__getitem__(key)
        except AttributeError:
            return replacement
