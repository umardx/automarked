from flask import render_template
from flask_login import login_required
from markupsafe import Markup

from app.dashboard.netconf import netconf
from app.models import Devices

import json


@netconf.route('/')
# @login_required
def index():
    devices = Devices.query.all()
    sample = """{
        "asbr": {
            "name": "asbr1",
            "address": "198.18.1.11"
        },
        "as": 65001,
        "interface": {
            "name": "GigabitEthernet0/0/0/0",
            "description": "Peering with AS65002",
            "address": "192.168.0.1",
            "netmask": 24
        },
        "neighbor": {
            "address": "192.168.0.2",
            "as": 65002
        }
    }"""
    response = Markup(json_dump(json.loads(sample)))

    return render_template(
        'dashboard/netconf/index.html',
        title='Netconf | Dashboard',
        response=response,
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
