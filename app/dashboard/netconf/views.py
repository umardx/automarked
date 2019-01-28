from flask import render_template
from flask_login import login_required

from app.dashboard.netconf import netconf
from app.models import Devices

import json


@netconf.route('/')
# @login_required
def index():
    devices = Devices.query.all()

    return render_template(
        'dashboard/netconf/index.html',
        title='Netconf | Dashboard',
        response='OKE',
        devices=devices
    )


def json_dump(dictionary):
    return json.dumps(dictionary, indent=4)


@netconf.route('/config')
@login_required
def config():

    return 'config'


@netconf.route('/operation')
@login_required
def operation():

    return 'operation'
