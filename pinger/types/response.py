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

    def __repr__(self):
        self.message


class InvalidStatusCode(ResponseError):
    message = 'Status code differs from expected status code'


class Response(object):
    """
    Pinger Response object.
    """

    name = None
    errors = None

    @property
    def ok(self):
        # Tells wether the request was successful or not
        return not self.errors
