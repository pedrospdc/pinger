from pinger.ext import ActionProvider


class SaveOnDb(ActionProvider):
    """
    Receives a response and saves into the configured database
    """
    title = 'SaveOnDb'

    def receive(self, status, errors, elapsed):
        print status, errors, elapsed
