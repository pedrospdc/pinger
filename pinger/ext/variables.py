import datetime
import os


variables = {
    'HOME_DIR': os.path.expanduser('~'),
    'CURRENT_DATE': datetime.datetime.now().strftime('%Y%m%d')
}


def interpolate_path(path):
    for key, val in variables.items():
        path = path.replace('%{key}%'.format(key=key), val)

    dir_path = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    return path
