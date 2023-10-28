from .unifiApi import Unifi
from multiprocessing import Pool
# from pymongo import MongoClient
# from socket import socket
import socket
# from bson import json_util
# from bson.json_util import dumps
#from bson.objectid import ObjectId
from pprint import pprint
# from termcolor import colored, cprint
import time
# import django
# # import os.path
# # import sys

# # # directory reach
# import sys
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainController.settings') 
# django.setup()

# directory = os.path.dirname(os.path.abspath("__file__"))
 
# print(directory)
# # setting path

# sys.path.append(os.path.dirname(os.path.dirname(directory)))
#sys.path.append('/.../mainController')
from .models import Devices 
#from models import Devices
# from mainController.models import models

def distributor(test):
    host = test[0]
    user = test[1]
    password = test[2]
    vendor = test[3]
    #print(test[1])
    host = host.rstrip()
    # cluster = MongoClient('mongodb://localhost:27017/prueba')
    # db = cluster['hotels']
    # collection = db[test[4]]
    collection = 'test'
    if vendor == 'unifi':
        connectUnifi(host, user, password, collection)

def checkHost(host):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		result = sock.connect_ex((host,22))
		sock.close()
		return result


def connectUnifi(host, user, password, collection):
    if checkHost(host) == 0:
        unifi = Unifi(host, user, password)
        if unifi.check_connection() == True:
            data = unifi.getData()
            print(data)
            if "model" not in data:
                print("error unifi "+host)
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

                    # Intenta actualizar el dispositivo existente o crear uno nuevo si no existe
                device, created = Devices.objects.update_or_create(
                    ipAddress=host,  # Condición de búsqueda: campo ipAddress
                    defaults=device_data  # Valores para actualizar o crear
                )

                if created:
                    print('Nuevo dispositivo creado:', device)
                else:
                    print('Dispositivo existente actualizado:', device)            
                # device = Devices(
                #      userName = user,
                #      ipAddress = host,
                #      hostName =  data['hostname'],
                #      model = data['model'],
                #      macAddress = data['mac address'],
                #      version = data['version'],
                #      controllerStatus = data['status'],
                #      status = 1,

                #      )
                # device.save()           

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
    hosts = [['10.2.2.30', 'n1mbu5','n3tw0rks','unifi','prueba'],['10.2.2.31', 'n1mbu5','n3tw0rks','unifi','prueba']]
    return hosts

def main():
    start = time.time()
    hosts = getHosts()
    pprint(hosts)
    mydict = []

    for host in hosts:
         distributor(host)
    # pool = Pool(10)

    # pool.map(distributor,hosts)

    finish = time.time()
    print(float("{:.2f}".format(finish - start)))

if __name__ == "__main__":
    main()