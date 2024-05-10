from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from bson import ObjectId
from rest_framework import generics
from collections import Counter
from openpyxl import load_workbook
from .models import Devices, GroupDevices
from .controller import main, checkHost, scan_devices, update_device_info
from .tools import _read_excel,unifi_controller,connect_mikrotik
from django.conf import settings
import os
from .serializers import GroupDevicesSerializer, DevicesSerializer
# from ._controller import connectRuckus
import json

class DevicesListCreateView(generics.ListCreateAPIView):
    serializer_class = DevicesSerializer

    def get_queryset(self):
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
    device = Devices.objects.get(pk=ObjectId(pk))
    return render(request, 'device_detail.html', {'device': device})

def update_device(request, macAddress):

    device = Devices.objects.get(macAddress=macAddress)
    update_device_info(device.ipAddress, device.deviceUser, device.devicePassword, device.group_id)
    return "ok"

class DevicesDetailView(DetailView):
    model = Devices
    serializer_class = DevicesSerializer
    template_name = 'device_detail.html'  # Nombre del template HTML

def devices_api(request):
    devices = Devices.objects.all()
    data = [{'host_name': device.deviceName, 'ip_address': device.ipAddress, 'model': device.model, 'model': device.macAddress, 'model': device.version,'model': device._id,} for device in devices]
    return JsonResponse({'devices': data})

def inicio(request):
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    for group in groups:
        print(group.__dict__)
    return render(request, 'dashboard.html', {'groups': groups})

def view_group(req, group):
    
    return render(req, 'group.html', {'group': group})

def test(req):
    resultado = main()
    return HttpResponse(resultado)    

def crear_grupo(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        print(group_name)
        nuevo_grupo = GroupDevices.objects.create(group_name=group_name)
        print(nuevo_grupo.__dict__)
        return render(request, 'group.html', {'group': group_name})
    else:
        return render(request, 'crear_grupo.html')

def view_groups(request):
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    print(groups.__dict__)
    for group in groups:
        print(group)
    return render(request, 'dashboard.html', {'groups': groups})

def view_gateway(request, group_id):
    contexto = 'ok'
    return render(request, 'gateway.html', contexto)

def view_access_points(request, group_id):
    dispositivos = Devices.objects.filter(group__group_name=group_id)
    status_counts = Counter(dispositivo.status for dispositivo in dispositivos)
    resultados = []
    status_counts_dict = {}
    for dispositivo in dispositivos:
        print(dispositivo._id)
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
    contexto = {
        'dispositivos': resultados,
        'status_counts_dict': status_counts_dict,
        'group_name': group_id,
    }
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
            else:
                print(f'{ip} no responde')

            print(resultado)
        scan_devices(devices_list)
        return redirect('ViewAccessPoints',group_id=group)
    else:
        return render(request, 'add_devices.html', {'group' : group})

def delete_device(request, pk):
    # Encuentra el dispositivo por su ID, si no existe, retorna un error 404
    dispositivo = get_object_or_404(Devices, pk=ObjectId(pk))
    grupo_perteneciente = dispositivo.group
    group_name = grupo_perteneciente.group_name    
    dispositivo.delete()
    return redirect('ViewAccessPoints',group_id=group_name)

def delete_all(request):
    Devices.objects.all().delete()
    return render(request, 'confirmacion.html')

def uc_connect(request):
    data = unifi_controller()
    return HttpResponse(data)

def mkt_connect(request):
    data = connect_mikrotik()
    return HttpResponse(data)

def read_excel(request):
    data = _read_excel()
    return HttpResponse(data)

# def connect_to_ruckus_ap(Request):    
#     print("intentando conectar")
#     connectRuckus('10.9.21.14','n1mbu5','n3tw0rks.')
#     return HttpResponse("ok")