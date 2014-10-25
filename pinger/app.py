import os

from pinger.exceptions import ConfigException
from pinger.settings import Config


class PingerApp(object):
    config = None

    def _load_config(self):
        if 'PINGER_SETTINGS' not in os.environ:
            raise ConfigException('The environment variable PINGER_SETTINGS must be set.')
        self.config = Config(os.environ['PINGER_SETTINGS'])
