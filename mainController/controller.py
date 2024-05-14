from django.db import transaction
from django.shortcuts import get_object_or_404
from multiprocessing import Pool
import routeros_api
import uuid
import socket
import json
from pprint import pprint
import time
from .models import Devices, GroupDevices
from .unifiApi import Unifi
from .ruckusApi import Ruckus
from .brocadeApi import Brocade
from .mikrotikApi import Mikrotik

def distributor(test):
    ip_address, user, password, vendor, collection = (test[0], test[1], test[2], test[3], test[4].rstrip())
    if vendor == 'unifi':
        connect_device(Unifi, ip_address, user, password, collection, vendor)
    elif vendor == 'ruckus':
        connect_device(Ruckus, ip_address, user, password, collection, vendor)
    elif vendor == 'brocade':
        connect_device(Brocade, ip_address, user, password, collection, vendor)
    elif vendor == 'mikrotik':
        print('mikrotik')
        connect_device(Mikrotik, ip_address, user, password, collection,vendor)        

def checkHost(ip_address, vendor):
    if vendor == 'mikrotik':
        port = 8728
    else:
        port = 22
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return not sock.connect_ex((ip_address, port))

def connect_device(DeviceClass, ip_address, user, password, collection, vendor):
    print("sigue ip")
    print(ip_address)
    if checkHost(ip_address, vendor):
        print('responde')
        device = DeviceClass(ip_address, user, password)
        if device.status == 1:
            hostname = device.getDeviceName()
            group = GroupDevices.objects.get(group_name=collection)
            data = device.getData()
            device_data = {
                'group': group,
                'deviceUser': user,
                'devicePassword': password,
                'ipAddress': ip_address,
                'deviceName': hostname,
                'model': data.get('model', ''),
                'macAddress': data.get('mac address', ''),
                'vendor': vendor,
                'version': data.get('version', ''),
                'controllerStatus': 'null',
                'clientes': {},
                'status': 2,
            }
            print(device_data)
            Devices.objects.update_or_create(ipAddress=ip_address, defaults=device_data)
        else:
            print(ip_address+'no responde')

def connect_device_update(DeviceClass, ip_address, user, password, collection):
    if checkHost(ip_address):
        print(ip_address)
        device = DeviceClass(ip_address, user, password)
        if device.status == 1:
            interfaces = device.getInterfacesDevices()
            #print(data)
            device_data = {
                'clientes': interfaces,
            }
            print(device_data)
            Devices.objects.update_or_create(ipAddress=ip_address, defaults=device_data)

def getHosts():
    return [['10.9.21.14', 'n1mbu5', 'n3tw0rks.', 'ruckus', 'hotel_a']]
 
def scan_devices(devices):
    with transaction.atomic():
        for host in devices:
            distributor(host)

def update_device_info(ip_address, user, password, collection):
    connect_device_update(Brocade, ip_address, user, password, collection)
    return "ok"

def connect_mikrotik(device):
    print(device)
    connection = routeros_api.RouterOsApiPool(device[0], username=device[1], password=device[2])
    api = connection.get_api()
    list_dhcp = api.get_resource('/ip/dhcp-server/lease')
    routerboard = api.get_resource('/system/routerboard')
    identity = api.get_resource('/system/identity')    
    _identity = identity.get()    
    interfaces = api.get_resource('/interface/ethernet')
    _routerboard = routerboard.get()
    _identity = identity.get()
    for interface in interfaces.get():
        if interface['name']=='ether1':
            mac_address=interface['mac-address']
    version =_routerboard[0]['current-firmware']
    model =_routerboard[0]['model']
    dhcp_list = list_dhcp.get()
    group = GroupDevices.objects.get(group_name=device[3])
    list_client = []
    for dhcp_client in dhcp_list:
        if 'mac-address' in dhcp_client and dhcp_client['mac-address']:
            list_client.append({
                'address':dhcp_client['address'],
                'mac':dhcp_client['mac-address'],
                'server':dhcp_client['server']
                })
    device_data = {
        'group': group,
        'deviceUser': device[1],
        'devicePassword': device[2],
        'ipAddress': device[0],
        'deviceName': _identity[0]['name'],
        'model': model,
        'macAddress': mac_address,
        'version': version,
        'controllerStatus': 'null',
        'clientes': list_client,
        'status': 2,
    }
    Devices.objects.update_or_create(ipAddress=device[0], defaults=device_data)


def main():
    start = time.time()
    hosts = getHosts()
    pprint(hosts)
    with transaction.atomic():
        for host in hosts:
             distributor(host)
    finish = time.time()
    print(float("{:.2f}".format(finish - start)))

if __name__ == "__main__":
    main()
