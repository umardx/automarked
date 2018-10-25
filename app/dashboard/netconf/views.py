from flask import flash, render_template, request
from flask_login import login_required

from app.dashboard.netconf import netconf
from app.models import ietf_interfaces
from pprint import pprint
from collections import OrderedDict
from ncclient import manager


@netconf.route('/')
# @login_required
def index():
    model = ietf_interfaces()

    ge1 = model.interfaces.interface.add('GigabitEthernet2')
    ipv4 = ge1.ipv4.address.add('167.205.3.1')
    ipv4.netmask = '255.255.255.0'
    ge1.description = 'NETCONF-CONFIGURED PORT'
    ge1.ipv4.mtu = 9000
    _ge1 = OrderedDict(ge1.get())
    pprint(_ge1)

    return 'index'


@netconf.route('/config')
@login_required
def config():

    return 'config'


@netconf.route('/operation')
@login_required
def operation():

    return 'operation'
