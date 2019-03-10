from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

from main.dashboard import views
