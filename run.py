# run.py

import os

from app import create_app, celery, socket_io

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
app.app_context().push()


if __name__ == '__main__':
    socket_io.run(app, host="0.0.0.0", port=8000, debug=True)
