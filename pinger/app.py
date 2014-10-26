import multiprocessing
import os
import time

from pinger.config import Config
from pinger.daemon import Daemon
from pinger.exceptions import ConfigException
from pinger.workers import watcher


class PingerApp(Daemon):
    """
    Pinger's main app
    """

    config = None

    def load_config(self):
        if 'PINGER_SETTINGS' not in os.environ:
            raise ConfigException('The environment variable PINGER_SETTINGS must be set.')
        self.config = Config(os.environ['PINGER_SETTINGS'])

    def callback(*args, **kwargs):
        print args, kwargs

    def run(self):
        while True:
            processes = []
            for i in self.config['websites']:
                p = multiprocessing.Process(target=watcher,
                                            args=(i['url'],
                                                  i['expected_content'],
                                                  i['expected_status_code'],
                                                  i.get('interval', self.config['default_interval']),
                                                  i.get('timeout', self.config['default_timeout'])))
                p.start()
                processes.append(p)

            for process in processes:
                process.join()

            time.sleep(self.config['main_process_sleep'])
