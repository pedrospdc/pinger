import datetime

import peewee

from pinger.app import get_current_app
from pinger.ext import ActionProvider
from pinger.ext.variables import interpolate_path


app = get_current_app()
path = interpolate_path(app.config['plugin_config']['sqlite']['database'])
db = peewee.SqliteDatabase(path)


class BaseModel(peewee.Model):
    """Base model"""

    class Meta:
        database = db


class Log(BaseModel):
    """
    Log base Model
    """

    website_name = peewee.CharField()
    website_url = peewee.TextField(index=True)
    status = peewee.BooleanField(index=True)
    # Elapsed time will be stored as microseconds
    elapsed = peewee.IntegerField(null=True)
    timestamp = peewee.DateTimeField(default=datetime.datetime.now, index=True)


class Error(BaseModel):
    log = peewee.ForeignKeyField(Log, related_name='errors')
    name = peewee.CharField(index=True)
    message = peewee.TextField()
    expected_result = peewee.CharField()
    actual_result = peewee.CharField()


class SQLite(ActionProvider):
    """
    Receives a response and saves into the configured database.

    Expects the following settings:

    ```
    {"sqlite": {"database": "%HOME_DIR%/pinger/db.sqlite"}}
    ```
    """
    title = 'SQLite'

    def __init__(self, *args, **kwargs):
        super(SQLite, self).__init__(*args, **kwargs)
        db.connect()
        try:
            db.create_tables([Log, Error])
        except peewee.OperationalError:
            # This logic must be removed and added as a CLI command
            pass

    def receive(self, name, url, status, errors, elapsed):
        log = Log.create(website_name=name, website_url=url, status=status,
                         elapsed=elapsed.microseconds if elapsed else None)
        for error in errors:
            Error.create(log=log, name=error['name'], message=error['message'],
                         actual_result=error['actual_result'],
                         expected_result=error['expected_result'])
