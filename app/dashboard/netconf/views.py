from flask import flash, render_template, request
from flask_login import login_required

from app.dashboard.netconf import netconf


@netconf.route('/')
@login_required
def index():

    return ''


@netconf.route('/config')
@login_required
def config():

    return ''


@netconf.route('/operation')
@login_required
def operation():

    return ''
