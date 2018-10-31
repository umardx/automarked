from flask import render_template
from flask_login import login_required
from markupsafe import Markup

from app.dashboard.netconf import netconf
from app.models.ietf import ietf_interfaces
from app.models import Devices

import json


HOST = 'r1.udx'
PORT = 8321
USER = 'admin'
PASS = 'admin'


@netconf.route('/')
# @login_required
def index():
    devices = Devices.query.all()

    ge_name = "Interface Name"
    description = "Description"

    ip_addr = '0.0.0.0'
    netmask = '255.255.255.0'

    model = ietf_interfaces()
    model.interfaces.interface.add(ge_name)
    model.interfaces.interface[ge_name].description = description
    model.interfaces.interface[ge_name].ipv4.address.add(ip_addr)
    model.interfaces.interface[ge_name].ipv4.address[ip_addr].netmask = netmask
    response = Markup(json_dump(model.get()))

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
