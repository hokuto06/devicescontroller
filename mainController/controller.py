from django.db import transaction
import uuid
from .unifiApi import Unifi
from multiprocessing import Pool
import socket
from pprint import pprint
import time
from .models import Devices, GroupDevices

def distributor(test):
    ip_address = test[0]
    user = test[1]
    password = test[2]
    vendor = test[3]
    ip_address = ip_address.rstrip()
    collection = test[4]
    # collection = "grupo"
    # collection = 'test'
    if vendor == 'unifi':
        connectUnifi(ip_address, user, password, collection)

def checkHost(ip_address):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		result = sock.connect_ex((ip_address,22))
		sock.close()
		return result

def get_group_id(collection):
    try:
        # grupos = GroupDevices.objects.all()
        # for grupo in grupos:
        #     print(grupo.group_name)
        #     print(grupo.group_id)
        group = GroupDevices.objects.get(group_name=collection)
  
        return group  # Convierte el ID a cadena antes de devolverlo
    except GroupDevices.DoesNotExist:
        # Manejar el caso cuando no se encuentra el grupo con el nombre dado
        return None

def connectUnifi(ip_address, user, password, collection):
    if checkHost(ip_address) == 0:
        print(collection)
        unifi = Unifi(ip_address, user, password)
        if unifi.check_connection() == True:
            #group = get_group_id(collection)
            group = GroupDevices.objects.get(group_name=collection)

            data = unifi.getData()
            print(data)
            if "model" not in data:
                print("error unifi "+ip_address)
            else:
                device_data = {
                        '_id': str(uuid.uuid4()),
                        'group':group,
                        'deviceUser': user,
                        'devicePassword': password,
                        'ipAddress': ip_address,
                        'deviceName': data['hostname'],
                        'model': data['model'],
                        'macAddress': data['mac address'],
                        'version': data['version'],
                        'controllerStatus': data['status'],
                        'status': 1,
                    }

                    # Intenta actualizar el dispositivo existente o crear uno nuevo si no existe
                device, created = Devices.objects.update_or_create(
                    ipAddress=ip_address,  # Condición de búsqueda: campo ipAddress
                    defaults=device_data  # Valores para actualizar o crear
                )
                print(group)
                if created:
                    print('Nuevo dispositivo creado:', device)
                else:
                    print('Dispositivo existente actualizado:', device)


def setStatus(status, host, post, collection):
    # post["status"] = status
    # collection.find_one_and_update({"ipv4": host},
	# 								{"$set": post},
	# 								upsert=True)
    pass

def getHosts():
    # cluster = MongoClient('mongodb://localhost:27017/hotels')
    # db = cluster['hotels']
    # collection = db[col]
    # _collection = collection.find()
    # hosts = []
    # for x in _collection:
    #     hosts.append([x['ipv4'].rstrip(), x['user'], x['password'], x['vendor'], col])
    # return hosts
    hosts = [['10.2.2.51', 'n1mbu5','n3tw0rks','unifi','hotel_f'],['10.2.2.52', 'n1mbu5','n3tw0rks','unifi','hotel_f']]
    # hosts = [['10.2.2.50', 'n1mbu5','n3tw0rks','unifi','hotel_f']]
    return hosts

# def update_devices_info(col):
#     devices = Devices.objects.all()
#     list_devices = []
#     for device in devices:
#          list_devices.append([device., device.userName, device.])
#     pass
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

    ## Linux version
    # mydict = []
    # pool = Pool(10)
    # pool.map(distributor,hosts)

    finish = time.time()
    print(float("{:.2f}".format(finish - start)))

if __name__ == "__main__":
    main()