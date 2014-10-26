__all__ = ('ResponseError', 'InvalidStatusCode', 'InvalidContent', 'Response', 'Timeout')


class ResponseError(object):
    """
    Base response error object type
    Errors implementing this reference should provide the following attributes:

    =================  =======================
    message            Error message
    expected_result    Expected result
    actual_result      Actual result
    =================  =======================
    """
    message = 'Im not an error yet'
    expected_result = None
    actual_result = None

    def __init__(self, expected_result, actual_result):
        self.expected_result = expected_result
        self.actual_result = actual_result

    def __repr__(self):
        return 'ResponseError: {message}, ' \
               'expected result: {expected_result}, ' \
               'actual result: {actual_result}'.format(message=self.message,
                                                       expected_result=self.expected_result,
                                                       actual_result=self.actual_result)


class InvalidStatusCode(ResponseError):
    message = 'Status code differs from expected status code'


class InvalidContent(ResponseError):
    message = 'Expected content not found on request content'


class Timeout(ResponseError):
    message = 'Request timed out'


class Response(object):
    """
    Pinger Response object.
    """

    name = None
    elapsed = None
    errors = []

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{name} status={status}>'.format(name=self.name, status=self.ok)

    @property
    def ok(self):
        # Tells wether the request was successful or not
        return not self.errors

    def add_error(self, error):
        self.errors.append(error)

    def set_elapsed_time(self, elapsed_time):
        self.elapsed = elapsed_time
