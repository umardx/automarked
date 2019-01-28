from ydk.services import CRUDService
from ydk.providers import  NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_cfg


def create_iface_configs(iface_configs):
    iface_config = iface_configs.InterfaceConfiguration()
    iface_config.link_status = ifmgr_cfg.Empty()


provider = NetconfServiceProvider(
    address='10.10.20.170',
    port=8321,
    username='admin',
    password='admin'
)

crud = CRUDService()

interface_configurations = ifmgr_cfg.InterfaceConfigurations()

create_iface_configs(
    iface_configs=interface_configurations
)

# create configuration on NETCONF device
crud.create(provider, interface_configurations)

exit()
