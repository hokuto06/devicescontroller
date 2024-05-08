from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import generics
from collections import Counter
from openpyxl import load_workbook
from .models import Devices, GroupDevices
from .controller import main, checkHost, scan_devices
from .tools import _read_excel,unifi_controller,connect_mikrotik
from django.conf import settings
import os
from .serializers import GroupDevicesSerializer, DevicesSerializer
# from ._controller import connectRuckus
import json

## Class Views
###############
#rest frawmeworks
class DevicesListCreateView(generics.ListCreateAPIView):
    serializer_class = DevicesSerializer

    def get_queryset(self):
        # Obtiene el parámetro group de la URL
        group = self.kwargs.get('group', None)
        print(group)
        # Filtra los dispositivos por group si está presente
        queryset = Devices.objects.all()
        if group is not None:
            queryset = queryset.filter(group=group)

        return queryset

class GroupDevicesListCreateView(generics.ListCreateAPIView):
    queryset = GroupDevices.objects.all()
    serializer_class = GroupDevicesSerializer


def device_detail_view(request, pk):
    device = Devices.objects.get(pk=pk)
    serializer = DevicesSerializer(device)
    return JsonResponse(serializer.data)

class DevicesDetailView(DetailView):
    model = Devices
    serializer_class = DevicesSerializer
    template_name = 'device_detail.html'  # Nombre del template HTML

#     @method_decorator(ensure_csrf_cookie)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def render_to_response(self, context, **response_kwargs):
#         # print(self.request.headers)
#         print(self.request.headers)
#         if 'HTTP_X_REQUESTED_WITH' in self.request.headers and self.request.headers['HTTP_X_REQUESTED_WITH'].lower() == 'XMLHttpRequest':
#             # Si es una solicitud AJAX, devuelve una respuesta JSON
#             device = self.get_object()
#             serializer = self.get_serializer(device)
#             print(device)
#             return JsonResponse(serializer.data)
#         else:
#             # Si no es una solicitud AJAX, utiliza el comportamiento predeterminado
#             return super().render_to_response(context, **response_kwargs)



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
        # print(nuevo_grupo)
        print(nuevo_grupo.__dict__)
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
        print(dispositivo.__dict__)
        dispositivo_dict = {
            'id': 'dispositivo._id',
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
                print(ip)
                devices_list.append([ip, texto1, texto2, texto3, group])
                # connectUnifi(ip, texto1, texto2, "hotel_f")
            else:
                print(f'{ip} no responde')

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

def uc_connect(request):
    data = unifi_controller()
    return HttpResponse(data)

def mkt_connect(request):
    data = connect_mikrotik()
    return HttpResponse(data)

def read_excel(request):

    data = _read_excel()
    # Devuelve el contenido de las celdas en una respuesta HTTP o haz lo que necesites con él
    return HttpResponse(data)

# def connect_to_ruckus_ap(Request):    
#     print("intentando conectar")
#     connectRuckus('10.9.21.14','n1mbu5','n3tw0rks.')
#     return HttpResponse("ok")