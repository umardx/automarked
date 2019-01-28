from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_cfg
from ydk.types import Empty
from ydk.filters import YFilter

provider = NetconfServiceProvider(
    address='10.10.20.170',
    port=8321,
    username='admin',
    password='admin'
)

crud = CRUDService()

iface_configs = ifmgr_cfg.InterfaceConfigurations()
iface_config = iface_configs.InterfaceConfiguration()
iface_config.shutdown = Empty()

ipv4 = iface_config.ipv4_network.addresses.Primary()
iface_config.ipv4_network.addresses.primary = ipv4

iface_config.active = 'act'

iface_configs.interface_configuration.append(iface_config)

result = crud.read(provider, iface_configs)

codec = CodecService()
codec_provider = CodecServiceProvider(type='json')


print(codec.encode(codec_provider, result))
