from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import environ

app = Flask(__name__)
app.config.from_object('automarked.config')
app_name = str(environ.get('APP_NAME'))

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import automarked.views