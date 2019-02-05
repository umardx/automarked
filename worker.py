from os import getenv
from app import celery, create_app

config_name = getenv('FLASK_CONFIG')
app = create_app(config_name)
app.app_context().push()
