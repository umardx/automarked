# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
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

    app.register_blueprint(_home)
    app.register_blueprint(_auth, url_prefix='/auth')
    app.register_blueprint(_dashboard, url_prefix='/dashboard')

    return app