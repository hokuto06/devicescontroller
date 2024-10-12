import os
import sys
sys.path.append('/home/hokuto/devicescontroller/mainController')
from vszApi import connectVsz
from pymongo import MongoClient
import pandas as pd
from pprint import pprint
client = MongoClient("mongodb://localhost:27017/")  # Asegúrate de que MongoDB esté corriendo
db = client["vsz_db"]  # Nombre de tu base de datos
collection = db["devices"]  # Colección donde guardarás los dispositivos
db_controller = client["prueba"]
controller_collection = db_controller["mainController_devices"]


def get_save_devices_from_vsz():
    vsz = connectVsz('192.168.188.10')

    aps = vsz.get_all_devices('test')

    if aps:
        collection.insert_many(aps)

# get_save_devices_from_vsz()

def insert_devices_on_excel():
    cursor = collection.find({})

    list_of_docs = list(cursor)

    df = pd.DataFrame(list_of_docs)

    df.to_excel('output.xlsx', index=False, engine='openpyxl')

    print("Datos guardados en 'output.xlsx'")

# insert_devices_on_excel

def update_devices_uplinks():
    cursor = controller_collection.find({"deviceType":"switch"})
    aps = collection.find({})
    list_of_aps = list(aps)
    list_of_docs = list(cursor)

    for aps in list_of_aps:
        # print(aps['mac'])        
        
        for switch in list_of_docs:
            nodo_padre = 'none'
            port_uplink = 'none'
            # break
            for ifc, mac in switch["clientes"].items():
                if mac.upper() == aps['mac']:
                    print(mac, aps['name'])
                    # print(aps['_id'])
                    nodo_padre = switch["deviceName"]
                    port_uplink = ifc
                    new_values = { "$set": {'nodo_padre':nodo_padre , 'port_uplink':port_uplink}}
                    filter = {'_id':aps['_id']}
                    collection.update_one(filter, new_values) 
                    break


# update_devices_uplinks()
insert_devices_on_excel()