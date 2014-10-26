from pinger.app import PingerApp


def main():
    app = PingerApp('/tmp/pinger.pid', stdout='/dev/stdout', stdin='/dev/stdin', stderr='/dev/stdin')
    app.load_config()
    app.load_plugins()
    app.run()
