from django.db import transaction
from django.shortcuts import get_object_or_404
from multiprocessing import Pool
import routeros_api
import uuid
import socket
from pprint import pprint
import time
from .models import Devices, GroupDevices
from .unifiApi import Unifi
from .ruckusApi import Ruckus
from .brocadeApi import Brocade

def distributor(test):
    ip_address, user, password, vendor, collection = (test[0], test[1], test[2], test[3], test[4].rstrip())
    if vendor == 'unifi':
        connect_device(Unifi, ip_address, user, password, collection)
    elif vendor == 'ruckus':
        connect_device(Ruckus, ip_address, user, password, collection)
    elif vendor == 'brocade':
        connect_device(Brocade, ip_address, user, password, collection)

def checkHost(ip_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return not sock.connect_ex((ip_address, 22))

def connect_device(DeviceClass, ip_address, user, password, collection):
    if checkHost(ip_address):
        device = DeviceClass(ip_address, user, password)
        if device.status == 1:
            hostname = device.getDeviceName()
            group = GroupDevices.objects.get(group_name=collection)
            data = device.getData()
            #print(data)
            device_data = {
                'group': group,
                'deviceUser': user,
                'devicePassword': password,
                'ipAddress': ip_address,
                'deviceName': hostname,
                'model': data.get('model', ''),
                'macAddress': data.get('mac address', ''),
                'version': data.get('version', ''),
                'controllerStatus': 'null',
                'clientes': {},
                'status': 2,
            }
            Devices.objects.update_or_create(ipAddress=ip_address, defaults=device_data)

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

def connect_mikrotik(devices):
    connection = routeros_api.RouterOsApiPool(devices[0], username=devices[1], password=devices[2])
    api = connection.get_api()
    list_dhcp = api.get_resource('/ip/dhcp-server/lease')
    routerboard = api.get_resource('/system/routerboard')
    identity = api.get_resource('/system/identity')
    dhcp_list = list_dhcp.get(server="dhcp1")
    print(dhcp_list)
    list_client = {}
    for dhcp_client in dhcp_list:
        # list_client.append(dhcp_client['address'])
        # list_client.append(dhcp_client['mac-address'])
        # list_client.append(dhcp_client['server'])
        # list_client.append([dhcp_client['address'],dhcp_client['mac-address'],dhcp_client['server']])
        list_client.update({'address':dhcp_client['address'],'mac':dhcp_client['mac-address'],'server':dhcp_client['server']})
    return(list_client)

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
