import multiprocessing
import os
import time
import threading

from pinger.config import Config
from pinger.daemon import Daemon
from pinger.exceptions import ConfigException
from pinger.ext import ActionProvider
from pinger.workers import watcher, post_processor

local = threading.local()


get_current_app = lambda: getattr(local, 'app', None)


class PingerApp(Daemon):
    """
    Pinger's main app
    """

    config = None

    def load_config(self):
        if 'PINGER_SETTINGS' not in os.environ:
            raise ConfigException('The environment variable PINGER_SETTINGS must be set.')
        self.config = Config(os.environ['PINGER_SETTINGS'])

    def load_plugins(self):
        for plugin in self.config.get('plugins', []):
            __import__(plugin)

        local.plugins = []

        for Plugin in ActionProvider.plugins:
            local.plugins.append(Plugin())

    def set_thread_app(self):
        local.app = self

    def run(self):
        """
        Main loop
        """
        while True:
            processes = []
            result_queue = multiprocessing.Queue()
            for i in self.config['websites']:
                p = multiprocessing.Process(target=watcher,
                                            args=(i['url'],
                                                  i['expected_content'],
                                                  i['expected_status_code'],
                                                  i.get('interval', self.config['default_interval']),
                                                  i.get('timeout', self.config['default_timeout']),
                                                  result_queue),
                                            name=i['name'])
                p.start()
                processes.append(p)

                post_processor_process = multiprocessing.Process(target=post_processor,
                                                                 args=(result_queue,))
                post_processor_process.start()
                processes.append(post_processor_process)

            for process in processes:
                process.join()

            time.sleep(self.config['main_process_sleep'])
