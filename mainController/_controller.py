#Conecta a Dispositivos Unifi.
from .unifiApi import Unifi
from .ruckusApi import Ruckus
from multiprocessing import Pool
from .models import Devices
import socket
from pprint import pprint
import time

def check_host(host):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((host, 22))
    sock.close()
    return result

def connect_unifi(host, user, password):
    if check_host(host) == 0:
        unifi = Unifi(host, user, password)
        if unifi.check_connection():
            data = unifi.get_data()
            print(data)
            if "model" not in data:
                print("Error en el dispositivo Unifi " + host)
            else:
                device_data = {
                    'userName': user,
                    'ipAddress': host,
                    'hostName': data['hostname'],
                    'model': data['model'],
                    'macAddress': data['mac address'],
                    'version': data['version'],
                    'controllerStatus': data['status'],
                    'status': 1,
                }

                device, created = Devices.objects.update_or_create(
                    ipAddress=host,
                    defaults=device_data
                )

                if created:
                    print('Nuevo dispositivo creado:', device)
                else:
                    print('Dispositivo existente actualizado:', device)

def connectRuckus(host, user, password):
    if check_host(host) == 0:
        ruckus = Ruckus(host, user, password)
        if ruckus.status == 1:
            print("ok")


def distributor(test):
    host, user, password, vendor, collection = test
    host = host.rstrip()
    if vendor == 'unifi':
        connect_unifi(host, user, password)

def get_hosts():
    hosts = [['10.2.2.25', 'n1mbu5', 'n3tw0rks', 'unifi', 'prueba'],
             ['10.2.2.26', 'n1mbu5', 'n3tw0rks', 'unifi', 'prueba']]
    return hosts

def main():
    start = time.time()
    hosts = get_hosts()
    pprint(hosts)

    for host in hosts:
        distributor(host)

    finish = time.time()
    print(float("{:.2f}".format(finish - start)))

if __name__ == "__main__":
    main()
