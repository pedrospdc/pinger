from pinger.app import PingerApp


def main():
    app = PingerApp('/tmp/pinger.pid', stdout='/dev/stdout', stdin='/dev/stdin', stderr='/dev/stderr')
    app.load_config()
    app.set_thread_app()
    app.load_plugins()
    app.run()
