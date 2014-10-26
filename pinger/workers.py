# -*- coding: utf-8 -*-
import multiprocessing
import time

import requests

from pinger.types import Response, InvalidContent, InvalidStatusCode, Timeout
from pinger.ext import ActionProvider


def watcher(url, expected_content, expected_status_code, interval, timeout, queue):
    response = Response(multiprocessing.current_process().name)

    try:
        request_response = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        error = Timeout('Open page', 'Timed out after {} seconds'.format(timeout))
        response.add_error(error)
    else:
        response.set_elapsed_time(request_response.elapsed)

        if expected_status_code != request_response.status_code:
            error = InvalidStatusCode(expected_result=expected_status_code, actual_result=request_response.status_code)
            response.add_error(error)

        if expected_content not in request_response.text:
            error = InvalidContent(expected_result=expected_content, actual_result='Content of {}'.format(url))
            response.add_error(error)

    queue.put(response.to_dict())
    time.sleep(interval)
    return watcher(url, expected_content, expected_status_code, interval, timeout, queue)


def post_processor(queue):
    """
    Processes results from watcher. Expects the result to be a dict
    containing the following data:

    ==========  ==========================================================
    status      Wether the request was successful or not
    errors      List of errors, each one being a dictionary itself.
    elapsed     Time taken for the request to be done
    ==========  ==========================================================
    """
    while True:
        response = queue.get()
        for Plugin in ActionProvider.plugins:
            plugin = Plugin()
            plugin.receive(status=response['status'], errors=response['errors'], elapsed=response['elapsed'])
