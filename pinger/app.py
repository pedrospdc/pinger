import os

from pinger.exceptions import ConfigException
from pinger.config import Config


class PingerApp(object):
    """
    Pinger's main apply
    """

    config = None

    def load_config(self):
        if 'PINGER_SETTINGS' not in os.environ:
            raise ConfigException('The environment variable PINGER_SETTINGS must be set.')
        self.config = Config(os.environ['PINGER_SETTINGS'])
