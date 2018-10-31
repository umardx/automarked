from flask import render_template
from flask_login import login_required

from app.dashboard.netconf import netconf
from app.models.ietf import ietf_interfaces
from app.models import Devices

from ncclient import manager
import xmltodict
import json


HOST = 'r1.udx'
PORT = 8321
USER = 'admin'
PASS = 'admin'


@netconf.route('/')
# @login_required
def index():
    devices = Devices.query.all()

    ge_name = "GigabitEthernet2"
    description = "This is Description"

    ip_addr = '1.1.1.1'
    netmask = '255.255.255.0'

    model = ietf_interfaces()
    model.interfaces.interface.add(ge_name)
    model.interfaces.interface[ge_name].description = description
    model.interfaces.interface[ge_name].ipv4.address.add(ip_addr)
    model.interfaces.interface[ge_name].ipv4.address[ip_addr].netmask = netmask
    response = json_dump(model.get())

    return render_template(
        'dashboard/netconf/index.html',
        title='Netconf | Dashboard',
        response = response,
        devices=devices
    )


def json_dump(dictionary):
    return json.dumps(dictionary, indent=4)


def get_capabilities(HOST, PORT, USER, PASS):

    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'default'},
                         look_for_keys=False, allow_agent=False) as m:
        return m.server_capabilities


def get_config(HOST, PORT, USER, PASS):
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS,
                         hostkey_verify=False, device_params={'name': 'default'},
                         look_for_keys=False, allow_agent=False) as m:
        return m.get_config(source='running').data_xml


@netconf.route('/config')
@login_required
def config():

    return 'config'


@netconf.route('/operation')
@login_required
def operation():

    return 'operation'
