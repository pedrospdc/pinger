import json
import os

from pinger.exceptions import ConfigException


class Config(object):
    """
    Config handler object.
    """
    config = None

    def _set_config(self, config_file):
        if not os.path.exists(config_file):
            raise ConfigException('Could not find config file.')

        with open(config_file, 'r') as f_:
            try:
                self.config = json.loads(f_.read())
            except ValueError:
                raise ConfigException('Could not decode config file.')

    def __getitem__(self, key):
        if not self.config:
            if 'PINGER_SETTINGS' not in os.environ:
                raise ConfigException('The environment variable PINGER_SETTINGS must be set.')
            self._set_config(os.environ['PINGER_SETTINGS'])

        return self.config[key]
