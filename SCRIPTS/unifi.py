#Probado con python3.8.10
# from unificontrol import UnifiClient
# from pprint import pprint
# from openpyxl import load_workbook

# def unifi_controller():
#     uc_user = "admin"
#     # uc_pass = "Elrbsest1._1"
#     uc_pass = "Elrbsest1._1"
#     uc_site = "default"
#     client = UnifiClient(host="192.168.222.2",port="443",
#     username=uc_user, password=uc_pass, site=uc_site)
#     devices = client.list_devices()
#     list_devices = []
#     for device in devices:
#         list_devices.append(device.get('name',''))
#         list_devices.append(device['ip'])
#         # list_devices['config_network']['ip': '10.2.3.58']
#         list_devices.append(device['mac'])
#         list_devices.append(device['_id'])
#         # pprint(device)
#     pprint(list_devices)
#     # client.rename_ap('64f1ed0a9820483c86373c04','prueba')
#     print(serial)
#     # return(list_devices)
#     return 'ok'


import requests
import socket
from pymongo import MongoClient

# Conexión a MongoDB (ajusta según tu configuración)
client = MongoClient("mongodb://localhost:27017/")  # Asegúrate de que MongoDB esté corriendo
db = client["unifi_db"]  # Nombre de tu base de datos
collection = db["devices"]  # Colección donde guardarás los dispositivos


def checkhost(host):
    print(host,'<---host')
    if host != 'unknown':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            return not sock.connect_ex((host, 22))

# Definir la URL del login y la API
login_url = "https://192.168.222.2/api/auth/login"
devices_url = "https://192.168.222.2/proxy/network/api/s/default/stat/device"
session = requests.Session()

# Datos de autenticación
username = "admin"
password = "Elrbsest1._1"

try:
    # Hacer la solicitud de login
    response = session.post(login_url, json={
        "username": username,
        "password": password
    }, verify=False)
    
    if response.status_code == 200:
        print("Login exitoso")
        
        # Ahora puedes hacer la solicitud para obtener la lista de dispositivos
        devices_response = session.get(devices_url, verify=False)
        list_devices = []
        if devices_response.status_code == 200:
            devices = devices_response.json()["data"]  # La información está en el campo "data"
            print("Dispositivos conectados:")
            for device in devices:
                list_devices.append({'mac':device.get('mac'),
                                    'name':device.get('name'),
                                    'model':device.get('model'),
                                    'ip':device.get('ip'),
                })

                # Insertar los dispositivos en MongoDB
            if list_devices:
                collection.insert_many(list_devices)

                print(f"- Nombre: {device.get('name')}, Mac: {device.get('mac')}, Modelo: {device.get('model')}, IP: {device.get('ip')}")
            print(list_devices)
        else:
            print(f"Error al obtener la lista de dispositivos: {devices_response.status_code}")

    else:
        print(f"Error en el login: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error en la conexión: {e}")



