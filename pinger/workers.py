# -*- coding: utf-8 -*-
import multiprocessing
import time

import requests


def watcher(url, expected_content, expected_status_code, interval, timeout, queue):
    """
    Makes a request and validates the response. Response is sent to given queue to be
    processed afterwards by a different worker
    """
    response = {'name': multiprocessing.current_process().name,
                'url': url,
                'errors': [],
                'elapsed': None}

    try:
        request_response = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        # Cant validate a timed out request
        error = {'expected_result': 'Open page',
                 'actual_result': 'Timed out after {} seconds'.format(timeout),
                 'name': 'Timeout',
                 'message': 'Request timed out'}
        response['errors'].append(error)
    else:
        # Request finished successfully, validating...
        response['elapsed'] = request_response.elapsed

        # Checks status code
        if expected_status_code != request_response.status_code:
            error = {'expected_result': expected_status_code,
                     'actual_result': request_response.status_code,
                     'name': 'InvalidStatusCode',
                     'message': 'Status code differs from expected status code'}
            response['errors'].append(error)

        # Looks for expected content on response text
        if expected_content not in request_response.text:
            error = {'expected_result': expected_content,
                     'actual_result': 'Content of {}'.format(url),
                     'name': 'InvalidContent',
                     'message': 'Expected content not found on request content'}
            response['errors'].append(error)

    response['status'] = bool(not response['errors'] and response.get('elapsed'))

    # Inserts response into post processing queue
    queue.put(response)
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
    from pinger.app import local
    while True:
        response = queue.get()
        for plugin in local.plugins:
            plugin.receive(name=response['name'],
                           url=response['url'],
                           status=response['status'],
                           errors=response['errors'],
                           elapsed=response['elapsed'])
