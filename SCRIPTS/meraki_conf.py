import meraki
 
# Tu clave API de Meraki
API_KEY = '96f5e24182f8af985d94053d3691331602e5f2eb'
 
# Inicializa el dashboard de Meraki
dashboard = meraki.DashboardAPI(API_KEY)
 
# El serial del AP que quieres modificar
serial = 'Q3AC-KSFK-WFEZ'
 
# Configuración de la IP y el nombre del AP
nuevo_nombre = 'prueba'
# nueva_ip = '192.168.150.199'  # Asegúrate de que sea una IP válida en la VLAN 100
# vlan_id = 1
# gateway_ip = '10.8.159.1'
# subnet_mask = '255.255.255.0'  # La máscara de red para la VLAN 100
# dns_servers = ['10.8.159.1']
network_id = 'L_579838452023963115'
new_name = 'prueba'
 
# Modificar el nombre, la IP y configurar la VLAN para el AP
# response = dashboard.devices.updateNetworkDeviceUplink(
response = dashboard.devices.updateDevice(
    serial=serial,
    name=new_name,
    #lanIp=nueva_ip,       # Asignar la IP estática
    #vlan=vlan_id,          # Asignar la VLAN
    #usingStaticIp=True
)
 
# Ver la respuesta para confirmar los cambios
print(f"Respuesta de actualización: {response}")