from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import generics
from collections import Counter
from .models import Devices, GroupDevices
from .controller import main, checkHost, connectUnifi, scan_devices

from .serializers import GroupDevicesSerializer, DevicesSerializer

## Class Views
###############

class DevicesListCreateView(generics.ListCreateAPIView):
    queryset = Devices.objects.all()
    serializer_class = DevicesSerializer

class DevicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Devices.objects.all()
    serializer_class = DevicesSerializer

class GroupDevicesListCreateView(generics.ListCreateAPIView):
    queryset = GroupDevices.objects.all()
    serializer_class = GroupDevicesSerializer

def devices_api(request):
    devices = Devices.objects.all()
    data = [{'host_name': device.deviceName, 'ip_address': device.ipAddress, 'model': device.model, 'model': device.macAddress, 'model': device.version,'model': device._id,} for device in devices]
    return JsonResponse({'devices': data})

## funciones
#############
def inicio(request):
    # groups = GroupDevices.objects.all()
    # return render(request, 'dashboard.html', {'groups': groups})
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    for group in groups:
        print(group)
    return render(request, 'dashboard.html', {'groups': groups})

def view_group(req, group):
    
    return render(req, 'group.html', {'group': group})

def test(req):
    resultado = main()
    # Haz algo con el resultado, por ejemplo, retornarlo como una respuesta HTTP
    return HttpResponse(resultado)    

def crear_grupo(request):
    if request.method == 'POST':
        # Obtén los datos del formulario enviado por el usuario
        group_name = request.POST['group_name']
        print(group_name)
        # Crea un nuevo grupo utilizando el modelo Group
        nuevo_grupo = GroupDevices.objects.create(group_name=group_name)
        return render(request, 'group.html', {'group': group_name})
    else:
        # Si el método de solicitud no es POST, muestra el formulario de creación
        return render(request, 'crear_grupo.html')  # Asegúrate de tener un template llamado 'crear_grupo.html' para mostrar el formulario

def view_groups(request):
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    for group in groups:
        print(group)
    return render(request, 'dashboard.html', {'groups': groups})

def view_access_points(request, group_id):
    # Recupera todos los objetos Devices de la base de datos
    dispositivos = Devices.objects.filter(group__group_name=group_id)
    status_counts = Counter(dispositivo.status for dispositivo in dispositivos)
    # Crea una lista de diccionarios para almacenar los resultados
    resultados = []
    status_counts_dict = {}
    for dispositivo in dispositivos:
        # Agrega los atributos relevantes del objeto a un diccionario
        dispositivo_dict = {
            'id': dispositivo._id,
            'host_name': dispositivo.deviceName,
            'version': dispositivo.version,
            'mac_address': dispositivo.macAddress,
            'model': dispositivo.model,
            'ip_address': dispositivo.ipAddress,
            'status': dispositivo.status,
            'controller_status': dispositivo.controllerStatus,
        }
        resultados.append(dispositivo_dict)
        status_counts_dict = {
            'status_0_count': status_counts[0],  # Cantidad de dispositivos con status 0
            'status_1_count': status_counts[1],  # Cantidad de dispositivos con status 1
            'status_2_count': status_counts[2],  # Cantidad de dispositivos con status 2
        }
    # Crea un diccionario de contexto con la lista de dispositivos
    contexto = {
        'dispositivos': resultados,
        'status_counts_dict': status_counts_dict,
        'group_name': group_id,
    }

    # Renderiza el template con el diccionario de contexto y retorna la respuesta HTTP
    return render(request, 'table.html', contexto)

def device_detail(request, ipAddress):
    device = get_object_or_404(Devices, ipAddress=ipAddress)
    context = {'device': device}
    return render(request, 'device_detail.html', context)

def procesar_formulario(request, group):
    if request.method == 'POST':
        ip1 = request.POST.get('ip1')
        ip2 = request.POST.get('ip2')
        texto1 = request.POST.get('texto1')
        texto2 = request.POST.get('texto2')
        texto3 = request.POST.get('texto3')
        group = request.POST.get('grupo')
        # group = 'hotel_a'
        split_ip1 = ip1.split('.')
        split_ip2 = ip2.split('.')
        print(f'grupo: {group}')
        devices_list = []
        for i in range(int(split_ip1[3]), int(split_ip2[3])+1):
            ip = '.'.join(split_ip1[0:3])+'.'+str(i)
            resultado = checkHost(ip)
            if resultado:
                print(f'{ip} no responde')
            else:
                print(ip)
                devices_list.append([ip, texto1, texto2, texto3, group])
                # connectUnifi(ip, texto1, texto2, "hotel_f")

            print(resultado)
        scan_devices(devices_list)
        # Puedes hacer más operaciones con los datos aquí
        return redirect('ViewAccessPoints',group_id=group)
        #return render(request, 'table.html', {'group' : group})  # Redirigir a una página de resultado o donde desees
    else:
        return render(request, 'add_devices.html', {'group' : group})

def delete_device(request, device_id):
    # Encuentra el dispositivo por su ID, si no existe, retorna un error 404
    dispositivo = get_object_or_404(Devices, _id=device_id)
    
    grupo_perteneciente = dispositivo.group
    
    # Obtiene el group_name del grupo
    group_name = grupo_perteneciente.group_name    
    # group_id = dispositivo.group.group_id 
    # Elimina el dispositivo
    dispositivo.delete()
    
    # Redirige a una página de éxito o donde desees
    # return HttpResponse()
    # return render(request, 'table.html', {'group' : group_name})  # Redirigir a una página de resultado o donde desees
    return redirect('ViewAccessPoints',group_id=group_name)

# def delete_device(request, device_id):
#     # Encuentra el dispositivo por su ID, si no existe, retorna un error 404
#     dispositivo = get_object_or_404(Devices, _id=device_id)
    
#     # Obtiene el grupo al que pertenece el dispositivo
#     grupo_perteneciente = dispositivo.group
    
#     # Obtiene el group_name del grupo
#     group_name = grupo_perteneciente.group_name

#     # Elimina el dispositivo
#     dispositivo.delete()
    
#     # Redirige a una página de éxito o donde desees
#     return render(request, 'table.html', {'group' : group_name})  # Redirigir a una página de resultado o donde desees


def delete_all(request):
    # Elimina todos los registros de la tabla Devices
    Devices.objects.all().delete()
    
    # Puedes redirigir a una página de confirmación o realizar otras acciones necesarias
    return render(request, 'confirmacion.html')
