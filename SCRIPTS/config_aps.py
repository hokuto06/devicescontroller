import sys 
import os 
sys.path.append('/home/hokuto/devicescontroller/mainController')
# sys.path.append('/home/esteban/app/devicescontroller/mainController')
from pymongo import MongoClient
from unifiApi import Unifi
from tools import unifi_controller

# Conectar a la base de datos de MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Cambia la URL según tu configuración

# Seleccionar la base de datos y la colección
db = client['unifi_db']  # Cambia el nombre de tu base de datos
collection = db['devices']  # Cambia el nombre de tu colección



def get_devices():
    # unifi_controller('172.20.197.148','etw7f5dj')
    unifi_controller('192.168.188.10','etw7f5dj')


def set_ap_default(ip_address, user, password):
    device = Unifi(ip_address, user,password)
    command = device.sendCommand('mca-cli-op set-default\n')
    print(command)

def set_ap_controller(ip_address, user, password):
    device = Unifi(ip_address, user, password)
    # device.set_inform('172.20.197.148')
    device.set_inform('192.168.188.10')
    print('ok')

# set_ap_controller('10.10.7.40','ubnt','ubnt')
# get_devices()

def reset_all_devices():
    documentos = collection.find()

    # Iterar sobre los documentos e interactuar con ellos
    for documento in documentos:
        if documento['state'] == 1:
            set_ap_default(documento['ip'], 'nimbus', 'networks')
            resultado = collection.update_one({"_id":documento['_id']}, {"$set": {"status":"default"}})
            print(documento)  # Puedes reemplazar esto con la lógica set_ap_default que necesites
            break
    # Cerrar la conexión al finalizarstatusstatus
    client.close()

reset_all_devices()