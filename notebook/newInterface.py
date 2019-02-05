from ydk.services import CRUDService
from ydk.providers import  NetconfServiceProvider
from ydk.filters import YFilter
from ydk.types import Empty
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_cfg


def create_iface_configs(iface_configs, iface_name, description, ipv4_address, ipv4_netmask):
    iface_config = iface_configs.InterfaceConfiguration()
    iface_config.active = 'act'
    iface_config.interface_name = iface_name
    iface_config.description = description

    ipv4 = iface_config.ipv4_network.addresses.Primary()
    ipv4.address = ipv4_address
    ipv4.netmask = ipv4_netmask

    iface_config.ipv4_network.addresses.primary = ipv4

    iface_config.statistics.load_interval = 60
    iface_config.statistics.load_interval = YFilter.delete

    iface_config.shutdown = Empty()
    iface_config.shutdown = YFilter.delete

    iface_configs.interface_configuration.append(iface_config)


provider = NetconfServiceProvider(
    address='10.10.20.170',
    port=8321,
    username='admin',
    password='admin'
)

crud = CRUDService()

interface_configurations = ifmgr_cfg.InterfaceConfigurations()

create_iface_configs(
    iface_configs=interface_configurations,
    iface_name='GigabitEthernet0/0/0/2',
    description='Example descriptions',
    ipv4_address='192.168.2.5',
    ipv4_netmask='255.255.255.128'
)

# create configuration on NETCONF device
crud.update(provider, interface_configurations)

exit()
