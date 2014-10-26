# -*- coding: utf-8 -*-
import multiprocessing
import time

import requests

from pinger.types import Response, InvalidContent, InvalidStatusCode, Timeout


def watcher(url, expected_content, expected_status_code, interval, timeout, queue):
    response = Response(multiprocessing.current_process().name)

    try:
        request_response = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        error = Timeout('Open page', 'Timed out after {} seconds'.format(timeout))
        response.add_error(error)
    else:
        response.set_elapsed_time = request_response.elapsed

        if expected_status_code != request_response.status_code:
            error = InvalidStatusCode(expected_result=expected_status_code, actual_result=request_response.status_code)
            response.add_error(error)

        if expected_content not in request_response.text:
            error = InvalidContent(expected_result=expected_content, actual_result='Content of {}'.format(url))
            response.add_error(error)

    print response
    print response.errors
    queue.put(response)
    time.sleep(interval)
    return watcher(url, expected_content, expected_status_code, interval, timeout, queue)
