from xrospf import Cisco_IOS_XR_ipv4_ospf_cfg
from ncclient import manager
import pyangbind.lib.pybindJSON as pybindJSON
import json
import sys
import os

host = '10.10.0.200'
port = '830'
username = 'cisco'
password = 'cisco'

processid = '1'
areaid = '0'
interface0 = 'GigabitEthernet0/0/0/0'
interface1 = 'GigabitEthernet0/0/0/1'

model = Cisco_IOS_XR_ipv4_ospf_cfg()

newospf = model.ospf.processes.process.add(processid)
ospfarea = newospf.default_vrf.area_addresses.area_area_id.add(areaid)
ospfarea.running = "True"
networkadd = ospfarea.name_scopes
network0 = networkadd.name_scope.add(interface0)
network0.running = "True"
network1 = networkadd.name_scope.add(interface1)
network1.running = "True"

json_data = pybindJSON.dumps(model, mode='ietf')

with open('xr1ospf.json', 'w') as f:
    f.write(json_data)

## Json to XML
os.system('json2xml -t config -o xr1ospf.xml xrospf.jtox xr1ospf.json')

##  Send XML
exists = os.path.isfile('xr1ospf.xml')
if exists :
    def read_file(fn):
        with open(fn) as f:
            result = f.read()
        return result
    
    os.remove('xr1ospf.json')
    xml = read_file('xr1ospf.xml')
    os.remove('xr1ospf.xml')

    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
        reply = m.edit_config(target='candidate', config=xml)
        c = m.commit()

    print("Edit Config Success? {}".format(reply.ok))
    print("Commit Success? {}".format(c.ok))

else:
    print("XML File Does Not Exist")