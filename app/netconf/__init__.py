from flask import Blueprint

netconf = Blueprint('netconf', __name__)

from app.netconf import views
