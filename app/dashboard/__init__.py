from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

from app.dashboard import views
