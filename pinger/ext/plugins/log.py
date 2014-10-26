import datetime
import logging
import os

from pinger.app import get_current_app
from pinger.ext import ActionProvider


class Log(ActionProvider):
    """
    Receives a response and logs it. Creates the parent folder if it doesnt exists.

    Expects the following settings:

    ```
    {"plugin_config": {
        "log": {
            "path": "%HOME_DIR%/logs/%CURRENT_DATE%.log",
            "logger_name": "pinger",
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    }}
    ```

    Interpolates __path__ with:
    ===============  ======================================
    %HOME_DIR%       User home path
    %CURRENT_DATE%   Current date with a %Y%m%d format
    ===============  ======================================

    """
    title = 'Log'
    variables = {
        'HOME_DIR': os.path.expanduser('~'),
        'CURRENT_DATE': datetime.datetime.now().strftime('%Y%m%d')
    }

    def __init__(self, *args, **kwargs):
        app = get_current_app()
        config = app.config['plugin_config']['log']
        path = config['path']

        for key, val in self.variables.items():
            path = path.replace('%{key}%'.format(key=key), val)

        dir_path = os.path.abspath(os.path.dirname(path))
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        logger = logging.getLogger(config['logger_name'])
        handler = logging.FileHandler(path)
        formatter = logging.Formatter(config['format'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def receive(self, name, url, status, errors, elapsed):
        self.logger.info('name={name} url={url} '
                         'elapsed={elapsed} '
                         'status={status}'.format(name=name,
                                                  url=url,
                                                  status=status,
                                                  elapsed=elapsed))
        for error in errors:
            self.logger.error('error={name} message={message} '
                              'expected_result={expected_result} actual_result={actual_result}'.format(**error))
