from os import path
from pathlib import Path


def get_db_file(file):
    """
    getDbFile() define database's file path to
    `./automarked/database/app.db`
    """
    _db_dir = path.join(Path(path.dirname(__file__)).parent, 'database')
    Path(_db_dir).mkdir(parents=True, exist_ok=True)
    _db_file = 'sqlite:///{}'.format(path.join(_db_dir, file))
    return _db_file


SECRET_KEY = 'AAAAAH/2wCEAAwICAgJCAwJCQwRCwoLERUPDAwPFRgTExUTExgRDAwM'
RECAPTCHA_PUBLIC_KEY = '6LcnP44UAAAAAFCNi_E2F7DH8ItMEEtEWbLQHmN1'
RECAPTCHA_PRIVATE_KEY = '6LcnP44UAAAAANO81XH5bcY8rnduMc29D9EM3BIU'
SQLALCHEMY_DATABASE_URI = get_db_file('app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
TEMPLATES_AUTO_RELOAD = True
CACHE_SIZE = 0
