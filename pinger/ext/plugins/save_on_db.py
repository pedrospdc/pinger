from pinger.ext import ActionProvider


class SaveOnDb(ActionProvider):
    title = 'SaveOnDb'

    def receive(self, status, errors, elapsed):
        print status, errors, elapsed
