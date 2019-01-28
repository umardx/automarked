from flask import render_template
from flask_login import login_required
from markupsafe import Markup

from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg

from app.dashboard.netconf import netconf
from app.models import Devices

import json


@netconf.route('/')
# @login_required
def index():
    devices = Devices.query.all()

    ge_name = "Interface Name"
    description = "Description Interface Name"

    ip_addr = '10.10.10.10'
    netmask = '255.255.255.0'

    # crud_provider = NetconfServiceProvider(
    #     address='10.10.20.170',
    #     port=8321,
    #     username='admin',
    #     password='admin'
    # )
    codec_provider = CodecServiceProvider(type='json')

    # crud = CRUDService()
    codec = CodecService()

    if_configs = Cisco_IOS_XR_ifmgr_cfg.InterfaceConfigurations()
    if_config = if_configs.InterfaceConfiguration()
    if_config.active = 'act'
    if_config.interface_name = ge_name

    if_configs.interface_configuration.append(if_config)

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
