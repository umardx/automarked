from flask_login import login_required

from app.dashboard.netconf import netconf
from app.models.ietf import ietf_interfaces
import pyangbind.lib.pybindJSON as pybindJSON
import json


@netconf.route('/')
# @login_required
def index():
    model = ietf_interfaces()

    _interface = model.interfaces.interface.add('GigabitEthernet2')
    _addr = _interface.ipv4.address.add('172.20.20.1')

    _addr2 = _interface.ipv4.address.add('172.20.30.1')

    json_data = pybindJSON.dumps(model, mode='ietf')
    # print(json_data)

    response = json.dumps(model.get(), indent=4)

    return response


@netconf.route('/config')
@login_required
def config():

    return 'config'


@netconf.route('/operation')
@login_required
def operation():

    return 'operation'
