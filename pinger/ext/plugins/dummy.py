from pinger.ext import ActionProvider


class DummyPlugin(ActionProvider):
    """
    Receives a response and does nothing
    """
    title = 'Dummy'

    def receive(self, name, url, status, errors, elapsed):
        pass
