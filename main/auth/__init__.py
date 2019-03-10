from flask import Blueprint

auth = Blueprint('auth', __name__)

from main.auth import views
