from flask import flash, render_template, request
from flask_login import login_required

from app.dashboard.netconf import netconf


@netconf.route('/')
@login_required
def index():

    return 'index'


@netconf.route('/config')
@login_required
def config():

    return 'config'


@netconf.route('/operation')
@login_required
def operation():

    return 'operation'
