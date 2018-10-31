from flask import Blueprint

netconf = Blueprint('netconf', __name__)

from app.dashboard.netconf import views
from ncclient import manager

# https://www.programcreek.com/python/example/93204/ncclient.manager.connect
# https://github.com/xiaomatech/ops/blob/master/library/netconf.py
class Netconf():
    def __init__(self, host, port, username, password):
        self.connect = manager.connect(
            host=host,
            port=port,
            username=username,
            password=password,
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            device_params={'name': 'default'}
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exited")
        if self.connect.connected:
            self.connect.__exit__()
        return False

    def get_all(self):
        return self.connect.get().data_xml

    def get_running_config(self):
        return self.connect.get_config(source='running').data_xml

    def get_capability_server(self):
        return self.connect.server_capabilities
