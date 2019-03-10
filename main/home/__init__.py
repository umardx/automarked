from flask import Blueprint

home = Blueprint('home', __name__)

from main.home import views
