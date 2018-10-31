from os import path, urandom
from pathlib import Path


def get_db_file():
    """
    getDbFile() define database's file path to
    `./automarked/database/app.db`
    """
    _db_dir = path.join(Path(path.dirname(__file__)).parent, 'database')
    Path(_db_dir).mkdir(parents=True, exist_ok=True)
    _db_file = 'sqlite:///{}'.format(path.join(_db_dir, 'app.db'))
    return _db_file

def get_celery_file():
    """
    getCeleryFile() define database's file path to
    `./automarked/database/celery.db`
    """
    _db_dir = path.join(Path(path.dirname(__file__)).parent, 'database')
    Path(_db_dir).mkdir(parents=True, exist_ok=True)
    _db_file = 'sqlite:///{}'.format(path.join(_db_dir, 'celery.db'))
    return _db_file


BROKER_TRANSPORT = "sqlalchemy"
BROKER_HOST = get_celery_file()

SECRET_KEY = urandom(32)
SQLALCHEMY_DATABASE_URI = get_db_file()
SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True
CACHE_SIZE = 0
