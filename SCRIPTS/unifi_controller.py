# from unificontrol import UnifiClient
# from openpyxl import load_workbook

# def unifi_controller():
#     uc_user = "rsupport"
#     uc_pass = "elrbsestNF!25"
#     uc_site = "etw7f5dj"
#     client = UnifiClient(host="172.20.197.148",
#     username=uc_user, password=uc_pass, site=uc_site)
#     devices = client.adopt_device('78:45:58:ef:13:f1')
#     return 'ok'

# unifi_controller()

##########################################################################
##########################################################################
##########################################################################

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint

# Datos del controlador UniFi
controller_url = "https://172.20.197.148:8443/api/login"
username = "rsupport"
password = "elrbsestNF!25"
device_id = "66f8af48d51d7f60b1d50ac8"
new_ip = "192.168.222.100"  # Nueva IP estática que deseas asignar
new_name = "NuevoNombreAP"  # Nuevo nombre que deseas asignar al AP
controller_url_api = "https://172.20.197.148:8443/api/s/etw7f5dj"

# Autenticación
login_url = f"{controller_url}login"
payload = {"username": username, "password": password}
session = requests.Session()
login_response = session.post(controller_url, headers={"Accept":"application/json","Content-Type":"application/json"}, data=json.dumps(payload), verify=False)
api_data = login_response.json()
pprint(api_data)

if login_response.status_code == 200:
    print("Autenticación exitosa")

    # Endpoint para modificar el dispositivo
    update_device_url = f"{controller_url_api}/rest/device/{device_id}"

    # Datos que deseas actualizar (nombre e IP)
    update_payload = {
        # "name": new_name,           # Actualizar nombre
        'config_network': {'dns1': '192.168.222.1',
                            'gateway': '192.168.222.1',
                            'ip': '192.168.222.100',
                            'netmask': '255.255.255.0',
                            'type': 'static'}
    }

    # Enviar la solicitud PUT para actualizar el dispositivo
    response = session.put(update_device_url, json=update_payload, verify=False)

    if response.status_code == 200:
        print(f"El dispositivo {new_name} se actualizó con éxito.")
    else:
        print(f"Error al actualizar el dispositivo: {response.text}")
else:
    print("Error en la autenticación:", login_response.text)
