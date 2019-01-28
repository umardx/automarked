from ydk.services import CRUDService
from ydk.providers import  NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as xr_ifmgr_cfg


def create_ifaceConfigs(ifaceConfigs, iface_name, description, ipv4_address, ipv4_netmask):
    ifaceConfig = ifaceConfigs.InterfaceConfiguration()
    ifaceConfig.active = 'act'
    ifaceConfig.interface_name = iface_name
    ifaceConfig.description = description

    ipv4 = ifaceConfig.ipv4_network.addresses.Primary()
    ipv4.address = ipv4_address
    ipv4.netmask = ipv4_netmask

    ifaceConfig.ipv4_network.addresses.primary = ipv4

    ifaceConfig.statistics.load_interval = 30

    ifaceConfigs.interface_configuration.append(ifaceConfig)



provider = NetconfServiceProvider(
    address = '10.10.20.170',
    port = 8321,
    username = 'admin',
    password = 'admin'
)

crud = CRUDService()

interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()
create_ifaceConfigs(
    ifaceConfigs=interface_configurations,
    iface_name='GigabitEthernet0/0/0/1',
    description='Example descriptions',
    ipv4_address = '192.168.1.5',
    ipv4_netmask = '255.255.255.252'
)

# create configuration on NETCONF device
crud.create(provider, interface_configurations)

exit()
