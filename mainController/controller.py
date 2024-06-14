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
from .vszApi import connectVsz
from openpyxl import load_workbook
import os


def distributor(test):
    ip_address, user, password, vendor, collection, state = (test[0], test[1], test[2], test[3], test[4].rstrip(), test[5])
    if vendor == 'unifi':
        connect_device(Unifi, ip_address, user, password, collection, vendor, state)
    elif vendor == 'ruckus':
        connect_device(Ruckus, ip_address, user, password, collection, vendor, state)
    elif vendor == 'brocade':
        connect_device(Brocade, ip_address, user, password, collection, vendor, state)
    elif vendor == 'mikrotik':
        print('mikrotik')
        connect_device(Mikrotik, ip_address, user, password, collection,vendor, state)

def checkHost(ip_address, vendor):
    if vendor == 'mikrotik':
        port = 8728
    else:
        port = 22
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return not sock.connect_ex((ip_address, port))

def connect_device(DeviceClass, ip_address, user, password, collection, vendor, state="configured"):
    print("sigue ip")
    print(ip_address)
    if checkHost(ip_address, vendor):
        print('responde')
        device = DeviceClass(ip_address, user, password)
        if device.status == 1:
            hostname = device.getDeviceName()
            group = GroupDevices.objects.get(group_name=collection)
            data = device.getData()
            clients  = device.get_clients()
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
                'clientes': clients,
                'state': state,
                'serialNumber':data.get('serial', ''),
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

def first_setup_ruckus_list(devices):
    list_aps = []
    with transaction.atomic():
        for host in devices:
            new_ap = Ruckus(host[0], host[1], host[2], firstTime=True)
            if new_ap.status == 1:
                list_aps.append(host[0], host[1], 'n3tw0rks.')
        scan_devices(list_aps)

'''
FUNCIONES VSZ
'''

def set_ap_controller(devices):
    with transaction.atomic():
        for host in devices:
            device = Ruckus(host[0], host[1], host[2])
            if device.status == 1:
                hostname = device.setController()
                return "ok"  


def update_info_from_excel(mac_address,serial):
    file_path = 'excel.xlsx'

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return []
    try:
        workbook = load_workbook(file_path)
        worksheet = workbook.active
    except Exception as e:
        print(f"Error loading workbook: {e}")
        return []
    data = []
    for row in worksheet.iter_rows(values_only=True):
        data.append(list(row))
    for index, row in enumerate(data):
        if len(row) >= 5:
            try:
                values = [row[0],row[1],row[4]]
                # print(f"{row[0]}{row[1]}{row[2]}-{row[3]}-{row[4]}")
                # value = f"{row[0]}{row[1]}{row[2]}-{row[3]}-{row[4]}"
                worksheet.cell(row=int(index)+1, column=2, value=mac_address)
                worksheet.cell(row=int(index)+1, column=3, value=serial)
            except TypeError as e:
                print(f"Error concatenating row data: {e}")
        else:
            print("Row does not have enough elements")
    try:
        workbook.save(file_path)
        print(f"Datos escritos en la primera columna de la segunda hoja en '{file_path}' exitosamente.")
    except Exception as e:
        print(f"Error al guardar el workbook: {e}")
    workbook.close()
    return data


    return ['hostname','ip_address','description']

def put_ap_info_on_vsz(mac_address):
    hostname, ip_address, description = update_device_info(mac_address,'serial')
    new_ap = connectVsz(mac_address)
    if new_ap.search_ap() == "ok":
        new_ap.config_ap(hostname=hostname,ip_address=ip_address,description=description)
'''
FIN FUNCIONES VSZ.
'''

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
