# -*- coding: utf-8 -*-
import multiprocessing
import time

import requests

from pinger.types import Response, InvalidContent, InvalidStatusCode


def watcher(url, expected_content, expected_status_code, interval, timeout):
    request_response = requests.get(url, timeout=timeout)
    response = Response(multiprocessing.current_process().name)
    response.set_elapsed_time = request_response.elapsed

    if expected_status_code != request_response.status_code:
        error = InvalidStatusCode(expected_result=expected_status_code, actual_result=request_response.status_code)
        response.add_error(error)

    if expected_content not in request_response.text:
        error = InvalidContent(expected_result=expected_content, actual_result='Content of {}'.format(url))
        response.add_error(error)

    time.sleep(interval)
    return watcher(url, expected_content, expected_status_code, interval, timeout)
