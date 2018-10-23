from flask import Blueprint

netconf = Blueprint('netconf', __name__)

from app.dashboard.netconf import views
