from flask_login import login_required

from app.dashboard.netconf import netconf
from app.models.ietf import ietf_interfaces
import pyangbind.lib.pybindJSON as pybindJSON
import json


@netconf.route('/<int:device_id>')
# @login_required
def index(device_id):
    print('<Device id="{}"/>'.format(device_id))
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

    return response


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
