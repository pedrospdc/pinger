import multiprocessing
import time

import requests

from pinger.types import Response, InvalidContent, InvalidStatusCode


def watch(url, expected_content, expected_status_code, interval, timeout, auth=None):
    request_response = requests.get(url, auth=auth, timeout=timeout)
    response = Response(multiprocessing.current_process().name)

    if expected_status_code != request_response.status_code:
        error = InvalidStatusCode(expected_result=expected_status_code, actual_result=request_response.status_code)
        response.add_error(error)

    if expected_content not in request_response.text:
        error = InvalidContent(expected_content=expected_content, actual_result=request_response.text)
        response.add_error(error)

    time.sleep(interval)
    return response
