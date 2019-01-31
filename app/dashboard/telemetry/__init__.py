from flask import Blueprint

telemetry = Blueprint('telemetry', __name__)

from app.dashboard.telemetry import views
