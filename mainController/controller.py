from django.db import transaction
from django.shortcuts import get_object_or_404
from multiprocessing import Pool
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

def getHosts():
    return [['10.9.21.14', 'n1mbu5', 'n3tw0rks.', 'ruckus', 'hotel_a']]
 
def scan_devices(devices):
    with transaction.atomic():
        for host in devices:
            distributor(host)

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
