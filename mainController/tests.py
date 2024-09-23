# from django.test import TestCase

# Create your tests here.
# split_ip1 = '10.2.2.3'.split('.')
# split_ip2 = '10.2.2.10'.split('.')


# for i in range(int(split_ip1[3]), int(split_ip2[3])+1):
#     print('.'.join(split_ip1[0:3])+'.'+str(i))
            
#lista = ['ec:f1:ec:10:72    2    1 130M     24M   83   15  23389    3682   ESs      4001f              0  ACK         20              P 02:22:45 IEEE80211_MODE_11NG_HT20  1  WME']
# lista = []
# prueba = []
# if lista:    
#     for l in lista:
#         #test = l.split()
#         #for t in l.split():
#         t = l.split()
#         prueba.append({"mac":t[0]})
# else:
#     print("lista vacia")

# print(prueba)
# print(ip1[3])
# import re

# data = '''
# ADDR               AID CHAN TXRATE RXRATE RSSI IDLE  TXSEQ  RXSEQ  CAPS        STATE MAXRATE(DOT11) DHCP TIME_TO_IP HTCAPS   MODE PSMODE ASSOCTIME    IEs
# 22:5a:11:0a:2f:16    6    1 144M      1M   38   15    788     904   ESs      4001f              0               0              P 01:10:58 IEEE80211_MODE_11NG_HT20  1  WME
# a6:ec:f1:ec:10:72    1    1 144M     24M   51    0  12328    4021   ESs      4003f              0               0              P 00:39:01 IEEE80211_MODE_11NG_HT20  1  WME
# b2:9a:b2:64:73:54    3    1 144M     24M   40    0   1720    1511   ESs      4001f              0  ACK         10              P 00:13:34 IEEE80211_MODE_11NG_HT20  1  WME
# 64:d6:9a:8d:fc:34    4    1 130M     64M   38    0   1666    2573   ESs          f              0  ACK         30             RM 00:10:25 IEEE80211_MODE_11NG_HT20  0  WME
# 4c:ba:d7:45:d5:b8    2    1  58M      1M   14    0    372     663   ESs          f              0  ACK         20             PM 00:01:09 IEEE80211_MODE_11NG_HT20  0  WME
# '''
# # print(data)
# reg_lines = re.split(r"[~\r\n]+", data)
# lista = []
# for i in range(2, len(reg_lines)-1):
#     lines = reg_lines[i].split()
#     lista.append(lines[0])

# print(lista)
# from pymongo import MongoClient

# # Conectarse a MongoDB (cambiar la URI según sea necesario)
# client = MongoClient('mongodb://localhost:27017/')

# # Seleccionar la base de datos y la colección
# db = client['prueba']
# collection = db['mainController_devices']

# # Obtener todos los documentos de la colección
# devices = collection.find({"group_id":7,})

# # Imprimir los objetos
# for device in devices:
#     print(device['clientes'])


# for dispositivo in dispositivos:
#     print(dispositivo._id)
#     print(dispositivo.clientes)
#     print(dispositivo.serialNumber)
#     print(dispositivo.macAddress)
#     print(dispositivo.deviceName)
#     print(dispositivo.model)
#     print(dispositivo.ipAddress)

# import pandas as pd
# from pymongo import MongoClient

# # Conectarse a MongoDB (ajusta la URI según sea necesario)
# client = MongoClient('mongodb://localhost:27017/')
# db = client['prueba']
# collection = db['mainController_devices']

# # Obtener todos los documentos de la colección
# devices = collection.find()

# # Convertir los documentos a una lista de diccionarios
# device_list = []
# for device in devices:
#     device_list.append(device)
    

# # Crear un DataFrame de pandas
# df = pd.DataFrame(device_list)

# # Guardar el DataFrame en un archivo Excel
# df.to_excel('devices.xlsx', index=False)


from pymongo import MongoClient
from openpyxl import Workbook

# Conectarse a MongoDB (ajusta la URI si es necesario)
client = MongoClient('mongodb://localhost:27017/')
db = client['prueba']
collection = db['mainController_devices']

# Obtener todos los documentos de la colección
devices = collection.find({"group_id":7,"deviceType":"switch"})

# Crear un nuevo archivo Excel
wb = Workbook()
ws = wb.active
ws.title = "MainController Devices"

# Agregar los encabezados (asumiendo que todos los documentos tienen las mismas claves)
ws.append(["Puerto", "MAC Address"])

for device in devices:
    if 'clientes' in device:  # Verifica que la clave 'clientes' exista en el documento
        clientes = device['clientes']
        device_name = device['deviceName'].replace('SSH@', '')  # Quitar 'SSH@' del nombre
        
        for puerto, mac in clientes.items():
            ws.append([puerto, mac, device_name])

# Guardar el archivo Excel
wb.save('devices_openpyxl.xlsx')

print("Datos guardados en 'devices_openpyxl.xlsx'")
