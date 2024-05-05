# #Conecta a Dispositivos Unifi.
# from .unifiApi import Unifi
# from .ruckusApi import Ruckus
# from multiprocessing import Pool
# from .models import Devices
# import socket
# from pprint import pprint
# import time

# def check_host(host):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.settimeout(0.5)
#     result = sock.connect_ex((host, 22))
#     sock.close()
#     return result

# def connect_unifi(host, user, password):
#     if check_host(host) == 0:
#         unifi = Unifi(host, user, password)
#         if unifi.check_connection():
#             data = unifi.get_data()
#             print(data)
#             if "model" not in data:
#                 print("Error en el dispositivo Unifi " + host)
#             else:
#                 device_data = {
#                     'userName': user,
#                     'ipAddress': host,
#                     'hostName': data['hostname'],
#                     'model': data['model'],
#                     'macAddress': data['mac address'],
#                     'version': data['version'],
#                     'controllerStatus': data['status'],
#                     'status': 1,
#                 }

#                 device, created = Devices.objects.update_or_create(
#                     ipAddress=host,
#                     defaults=device_data
#                 )

#                 if created:
#                     print('Nuevo dispositivo creado:', device)
#                 else:
#                     print('Dispositivo existente actualizado:', device)

# def connectRuckus(host, user, password):
#     if check_host(host) == 0:
#         ruckus = Ruckus(host, user, password)
#         if ruckus.status == 1:
#             print("ok")


# def distributor(test):
#     host, user, password, vendor, collection = test
#     host = host.rstrip()
#     if vendor == 'unifi':
#         connect_unifi(host, user, password)

# def get_hosts():
#     hosts = [['10.2.2.25', 'n1mbu5', 'n3tw0rks', 'unifi', 'prueba'],
#              ['10.2.2.26', 'n1mbu5', 'n3tw0rks', 'unifi', 'prueba']]
#     return hosts

# def main():
#     start = time.time()
#     hosts = get_hosts()
#     pprint(hosts)

#     for host in hosts:
#         distributor(host)

#     finish = time.time()
#     print(float("{:.2f}".format(finish - start)))

# if __name__ == "__main__":
#     main()


# from django.db import transaction
# from django.shortcuts import get_object_or_404
# from multiprocessing import Pool
# import uuid
# import socket
# from pprint import pprint
# import time
# from .models import Devices, GroupDevices
# from .unifiApi import Unifi
# from .ruckusApi import Ruckus

# def distributor(test):
#     ip_address = test[0]
#     user = test[1]
#     password = test[2]
#     vendor = test[3]
#     ip_address = ip_address.rstrip()
#     collection = test[4]
#     # collection = "grupo"
#     # collection = 'test'
#     if vendor == 'unifi':
#         connectUnifi(ip_address, user, password, collection)
#     elif vendor == 'ruckus':
#         connectRuckus(ip_address, user, password, collection)

# def checkHost(ip_address):
# 		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 		sock.settimeout(0.5)
# 		result = sock.connect_ex((ip_address,22))
# 		sock.close()
# 		return result

# def get_group_id(collection):
#     try:
#         # grupos = GroupDevices.objects.all()
#         # for grupo in grupos:
#         #     print(grupo.group_name)
#         #     print(grupo.group_id)
#         group = GroupDevices.objects.get(group_name=collection)
  
#         return group  # Convierte el ID a cadena antes de devolverlo
#     except GroupDevices.DoesNotExist:
#         # Manejar el caso cuando no se encuentra el grupo con el nombre dado
#         return None

# def connectRuckus(ip_address, user, password, collection):
#     if checkHost(ip_address) == 0:
#         print(collection)
#         ruckus = Ruckus(ip_address, user, password)
#         print("sigue passw")
#         print(password)
#         print("sigue usuario")
#         print(user)
#         if ruckus.status == 1:
#         #if ruckus.check_connection() == True:
#             hostname = ruckus.getDeviceName()
#             group = GroupDevices.objects.get(group_name=collection)
#             data = ruckus.getData()
#             print(data)
#             device_data = {
#                     # '_id': str(uuid.uuid4()),
#                     'group':group,
#                     'deviceUser': user,
#                     'devicePassword': password,
#                     'ipAddress': ip_address,
#                     'deviceName': hostname,
#                     'model': data['model'],
#                     'macAddress': data['mac_address'],
#                     'version': data['version'],
#                     'controllerStatus': 'null',
#                     #'clientes': clients,
#                     'status': 2,
#                 }
#             # try:
#             #     existing_device = Devices.objects.get(ipAddress=ip_address)
#             #     pass
#             # except Devices.DoesNotExist:
#             #     existing_device = None
#             #     device_data["_id"] = str(uuid.uuid4())
#             #     # Intenta actualizar el dispositivo existente o crear uno nuevo si no existe
#             device, created = Devices.objects.update_or_create(
#                 ipAddress=ip_address,  # Condición de búsqueda: campo ipAddress
#                 defaults=device_data  # Valores para actualizar o crear
#             )
#             print(group)
#             if created:
#                 print('Nuevo dispositivo creado:', device)
#             else:
#                 print('Dispositivo existente actualizado:', device)


# def connectUnifi(ip_address, user, password, collection):
#     if checkHost(ip_address) == 0:
#         print(collection)
#         unifi = Unifi(ip_address, user, password)
#         if unifi.check_connection() == True:
#             #group = get_group_id(collection)
#             group = GroupDevices.objects.get(group_name=collection)
#             data = unifi.getData()
#             print(data)
#             if "model" not in data:
#                 print("error unifi "+ip_address)
#             else:
#                 clients =  unifi.getWlanClients()
#                 # if clients.index:
#                 #     wclients_list = []
#                 #     for wclients in data:
#                 #         wc = wclients.split()
#                 #         # wclients_list.append({"mac":t[0]})
#                 # else:
#                 #      wclients_list = 
#                 print(clients)
# # ********* Recorrer todas las interfaces ****  
#                 device_data = {
#                         # '_id': str(uuid.uuid4()),
#                         'group':group,
#                         'deviceUser': user,
#                         'devicePassword': password,
#                         'ipAddress': ip_address,
#                         'deviceName': data['hostname'],
#                         'model': data['model'],
#                         'macAddress': data['mac address'],
#                         'version': data['version'],
#                         'controllerStatus': data['status'],
#                         'clientes': clients,
#                         'status': 2,
#                     }
#                 # try:
#                 #     existing_device = Devices.objects.get(ipAddress=ip_address)
#                 #     pass
#                 # except Devices.DoesNotExist:
#                 #     existing_device = None
#                 #     device_data["_id"] = str(uuid.uuid4())
#                 #     # Intenta actualizar el dispositivo existente o crear uno nuevo si no existe
#                 # except Exception as e:
#                 #     print('sigue error')
#                 #     print(e)
#                 device, created = Devices.objects.update_or_create(
#                     ipAddress=ip_address,  # Condición de búsqueda: campo ipAddress
#                     defaults=device_data  # Valores para actualizar o crear
#                 )
#                 print(group)
#                 if created:
#                     print('Nuevo dispositivo creado:', device)
#                 else:
#                     print('Dispositivo existente actualizado:', device)


# def setStatus(status, host, post, collection):
#     # post["status"] = status
#     # collection.find_one_and_update({"ipv4": host},
# 	# 								{"$set": post},
# 	# 								upsert=True)
#     pass

# def getHosts():
#     # cluster = MongoClient('mongodb://localhost:27017/hotels')
#     # db = cluster['hotels']
#     # collection = db[col]
#     # _collection = collection.find()
#     # hosts = []
#     # for x in _collection:
#     #     hosts.append([x['ipv4'].rstrip(), x['user'], x['password'], x['vendor'], col])
#     # return hosts
#     hosts = [['10.9.21.14', 'n1mbu5','n3tw0rks.','ruckus','hotel_a']]
#     # hosts = [['10.2.2.50', 'n1mbu5','n3tw0rks','unifi','hotel_f']]
#     return hosts

# # def update_devices_info(col):
# #     devices = Devices.objects.all()
# #     list_devices = []
# #     for device in devices:
# #          list_devices.append([device., device.userName, device.])
# #     pass
# def scan_devices(devices):

#     with transaction.atomic():
#         for host in devices:
#             distributor(host)

# def main():
#     start = time.time()
#     hosts = getHosts()
#     pprint(hosts)

#     with transaction.atomic():
#         for host in hosts:
#              distributor(host)

#     ## Linux version
#     # mydict = []
#     # pool = Pool(10)
#     # pool.map(distributor,hosts)

#     finish = time.time()
#     print(float("{:.2f}".format(finish - start)))

# if __name__ == "__main__":
#     main()