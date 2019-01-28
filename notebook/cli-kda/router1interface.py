from xrinterface import Cisco_IOS_XR_ifmgr_cfg
from ncclient import manager
import pyangbind.lib.pybindJSON as pybindJSON
import json
import sys
import os
import xmltodict
import xml.etree.ElementTree as ET

def read_file(fn):
    with open(fn) as f:
        result = f.read()
    return result

def find_shutdown(data, act, iface_name):
    exist = False
    data_dict = xmltodict.parse(data, dict_constructor=dict)
    ifaces = data_dict['data']['interface-configurations']['interface-configuration']

    for iface in ifaces:
        if iface['active'] == act and iface['interface-name'] == iface_name:
            try:
                iface['shutdown']
                exist = True
            except:
                continue
    return exist
# adashutdown = find_shutdown(data=runconf, act='act', iface_name='GigabitEthernet0/0/0/2')
# print(adashutdown)

host = '10.10.0.200'
port = '830'
username = 'cisco'
password = 'cisco'

interface0 = 'act GigabitEthernet0/0/0/0'
inetrface1 = 'act GigabitEthernet0/0/0/1'

model = Cisco_IOS_XR_ifmgr_cfg()

## Add New Interface GigabitEthernet0/0/0/0
new_interface0 = model.interface_configurations.interface_configuration.add(interface0)

## IPv4 Configuration
ipv4add0 = new_interface0.ipv4_network.addresses.primary
ipv4add0.address = '10.10.1.1'
ipv4add0.netmask = '255.255.255.252'

## Add New Interface GigabitEthernet0/0/0/1
new_interface1 = model.interface_configurations.interface_configuration.add(inetrface1)

## IPv4 Configuration
ipv4add1 = new_interface1.ipv4_network.addresses.primary
ipv4add1.address = '10.10.1.5'
ipv4add1.netmask = '255.255.255.252'

json_data = pybindJSON.dumps(model, mode='ietf')

with open('xrinterface.json', 'w') as f:
    f.write(json_data)

## Json to XML
os.system('json2xml -t config -o xrinterface.xml xrinterface.jtox xrinterface.json')


with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
    interface_filter = '''
                          <filter>
                             <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                             </interface-configurations>
                          </filter>
                          '''
    reply = m.get_config(source='running', filter=interface_filter).data_xml
    with open("running_interface.xml", 'w') as f:
        f.write(reply)

runconf = read_file('running_interface.xml')

shutdown0 = find_shutdown(data=runconf, act='act', iface_name='GigabitEthernet0/0/0/0')
shutdown1 = find_shutdown(data=runconf, act='act', iface_name='GigabitEthernet0/0/0/1')

tree0 = ET.parse('xrinterface.xml')
root0 = tree0.getroot()

## No Shutdown
if shutdown0==True :
    ET.SubElement(root0[0][0],"ifmgr-cfg:shutdown").set('nc:operation',"delete")
    tree0.write('xrinterface.xml')
tree1 = ET.parse('xrinterface.xml')
root1 = tree1.getroot()
if shutdown1==True :
    ET.SubElement(root1[0][1],"ifmgr-cfg:shutdown").set('nc:operation',"delete")
    tree1.write('xrinterface.xml')
#os.remove('running_interface.xml')

# tree = ET.parse('xrinterface.xml')
# root = tree.getroot()
# ET.SubElement(root[0][0],"ifmgr-cfg:shutdown").set('nc:operation',"delete")
# tree.write('xrinterface.xml')

## Send XML
exists = os.path.isfile('xrinterface.xml')
if exists :

    #os.remove('xrinterface.json')
    xml = read_file('xrinterface.xml')
    #os.remove('xrinterface.xml')

    with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False, device_params={'name': 'iosxr'}) as m:
        reply = m.edit_config(target='candidate', default_operation='none', config=xml)
        c = m.commit()

    print("Edit Config Success? {}".format(reply.ok))
    print("Commit Success? {}".format(c.ok))

else:
    print("XML File Does Not Exist")
