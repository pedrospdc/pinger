from pinger.ext import ActionProvider


class StdOut(ActionProvider):
    """
    Receives a response and prints it
    """
    title = 'StdOut'

    def receive(self, name, url, status, errors, elapsed):
        print 'name={name} url={url} elapsed={elapsed} status={status}'.format(name=name,
                                                                               url=url,
                                                                               status=status,
                                                                               elapsed=elapsed.total_seconds() if elapsed else 'TIMEOUT')
        for error in errors:
            print 'error={name} message={message} ' \
                  'expected_result={expected_result} actual_result={actual_result}'.format(**error)
