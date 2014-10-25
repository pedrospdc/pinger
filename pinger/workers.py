import time

import requests

from pinger.types import Response


def watch(url, expected_content, expected_status_code, interval, timeout, auth=None):
    response = requests.get(url, auth=auth, timeout=timeout)

    if expected_status_code != response.status_code:
        return 

    if expected_content not in response.text:
        raise InvalidContent

    time.sleep(interval)
    return True
