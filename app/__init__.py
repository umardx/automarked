# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    sentry_sdk.init(
        dsn="https://849a6be889314c8ca7ac4267be19e734@sentry.io/1308772",
        integrations=[FlaskIntegration()]
    )

    app = Flask(__name__)
    app.config.from_object('app.config')
    
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.signin"

    migrate = Migrate(app, db)
    
    from app import models
    from app.home import home as _home
    from app.auth import auth as _auth
    from app.dashboard import dashboard as _dashboard
    from app.dashboard.netconf import netconf as _netconf

    app.register_blueprint(_home)
    app.register_blueprint(_auth, url_prefix='/auth')
    app.register_blueprint(_dashboard, url_prefix='/dashboard')
    app.register_blueprint(_netconf, url_prefix='/dashboard/netconf')

    return app
