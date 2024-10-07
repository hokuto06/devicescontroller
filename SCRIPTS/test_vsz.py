import os
import sys
sys.path.append('/home/hokuto/devicescontroller/mainController')
from vszApi import connectVsz
from pymongo import MongoClient
import pandas as pd
client = MongoClient("mongodb://localhost:27017/")  # Asegúrate de que MongoDB esté corriendo
db = client["vsz_db"]  # Nombre de tu base de datos
collection = db["devices"]  # Colección donde guardarás los dispositivos

def get_save_devices_from_vsz():
    vsz = connectVsz('192.168.188.10')

    aps = vsz.get_all_devices('test')

    if aps:
        collection.insert_many(aps)


cursor = collection.find({})  # Puedes aplicar un filtro si es necesario

# Convertir los documentos a una lista de diccionarios
list_of_docs = list(cursor)

# Crear un DataFrame a partir de la lista de documentos
df = pd.DataFrame(list_of_docs)

# Guardar en un archivo Excel
df.to_excel('output.xlsx', index=False, engine='openpyxl')

print("Datos guardados en 'output.xlsx'")