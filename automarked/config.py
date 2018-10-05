from os import path, urandom
from pathlib import Path

def getDbFile():
    """
    getDbFile() define database's file path to
    `./automarked/database/automarked.db`
    """
    _db_dir = path.join(Path(path.dirname(__file__)).parent, 'database')
    Path(_db_dir).mkdir(parents=True, exist_ok=True)
    _db_file = 'sqlite:///{}'.format(path.join(_db_dir, 'automarked.db'))
    return _db_file

SECRET_KEY = urandom(32)
SQLALCHEMY_DATABASE_URI = getDbFile()
SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True
CACHE_SIZE = 0