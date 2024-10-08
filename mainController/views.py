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
# from openpyxl import load_workbook
from .models import Devices, GroupDevices, Controllers
from .controller import main, checkHost, scan_devices, update_device_info,connect_mikrotik, distributor, set_ap_controller,put_ap_info_on_vsz, get_device_from_vsz
from .controller import aps_from_vsz, get_one_ap_from_vsz, set_single_ap_on_vsz, get_all_vsz_zones, get_all_groups_from_vsz_zones
from django.conf import settings
from django.contrib import messages
from .forms import UploadFileForm
import os
from .serializers import GroupDevicesSerializer, DevicesSerializer
import json

def upload_file(request, group_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Asegurarse de que el directorio de destino existe
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)
            # Guarda el archivo en el directorio especificado en settings.MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            messages.success(request, 'Archivo subido con éxito.')
            return redirect('setup', group_id=group_id)
    else:
        form = UploadFileForm()
    return render(request, 'setup.html', {'form': form, 'group_name': group_id})


class GroupDevicesListCreateView(generics.ListCreateAPIView):
    queryset = GroupDevices.objects.all()
    serializer_class = GroupDevicesSerializer
 
def device_detail_view(request, pk):
    device = Devices.objects.get(pk=ObjectId(pk))
    group_name = GroupDevices.objects.get(group_id=device.group_id)
    device_type = device.deviceType
    if device_type == 'router':
        device_clientes = device.clientes
    elif device_type == 'switch':
        device_clientes = list(device.clientes.items())
    else:
        device_clientes = []
    dispositivo_dict = {
        'id': device._id,
        'host_name': device.deviceName,
        'version': device.version,
        'mac_address': device.macAddress,
        'model': device.model,
        'ip_address': device.ipAddress,
        'group_name': group_name.group_name,
        'status': device.status,
        'state': device.state,
        'serial_number': device.serialNumber,
        'clientes':device_clientes,
        'controller_status': device.controllerStatus,
        'deviceType':device.deviceType,
    }
    return render(request, 'device_detail.html', {'device': dispositivo_dict,'group_name':group_name.group_name})

def setup_devices(request, group_id):
    dispositivos = Devices.objects.filter(group__group_name=group_id, state='default',vendor='ruckus')
    resultados = []
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
            'serial': dispositivo.serialNumber,
            'group_name': group_id,
            'controller_status': dispositivo.controllerStatus,
        }
        resultados.append(dispositivo_dict)

    contexto = {
        'dispositivos': resultados,
        'group_name': group_id,
    }
    return render(request, 'setup.html', contexto)

def devices_api(request):
    devices = Devices.objects.all()
    data = [{'host_name': device.deviceName, 'ip_address': device.ipAddress, 'model': device.model, 'model': device.macAddress, 'model': device.version,'model': device._id,} for device in devices]
    return JsonResponse({'devices': data})

def inicio(request):
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    return render(request, 'dashboard.html', {'groups': groups, 'group_name':groups[0].group_name})

def view_group(req, group):
    
    return render(req, 'group.html', {'group': group})

def test(req):
    resultado = main()
    return HttpResponse(resultado)    

def crear_grupo(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        # print(group_name)
        nuevo_grupo = GroupDevices.objects.create(group_name=group_name)
        # print(nuevo_grupo.__dict__)
        return render(request, 'group.html', {'group_name': group_name})
    else:
        return render(request, 'crear_grupo.html')

def view_groups(request):
    groups = GroupDevices.objects.annotate(num_devices=Count('devices'))
    print(groups.__dict__)
    for group in groups:
        print(group)
    return render(request, 'dashboard.html', {'groups': groups})

def view_vsz(request, group_id):
    contexto = {'group_name':group_id}
    return render(request, 'vsz.html', contexto )

def view_devices_by_type(request, group_id, device_type):
    dispositivos = Devices.objects.filter(group__group_name=group_id,deviceType=device_type)
    status_counts = Counter(dispositivo.status for dispositivo in dispositivos)
    resultados = []
    status_counts_dict = {}
    device_type_mapping = {'router': 'Gateway','switch': 'Switches','access_point': 'Access Points'}
    deviceType = device_type_mapping.get(device_type, 'Unknown')
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
        'device_type': deviceType,
    }
    return render(request, 'viewdevices.html', contexto)


def view_gateway(request, group_id):
    return view_devices_by_type(request, group_id, 'router')

def view_access_points(request, group_id):
    return view_devices_by_type(request, group_id, 'access_point')

def view_access_switchs(request, group_id):
    return view_devices_by_type(request, group_id, 'switch')


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
        return render(request, 'add_devices.html', {'group_name' : group})

def add_one(request, group):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        texto1 = request.POST.get('texto1')
        texto2 = request.POST.get('texto2')
        texto3 = request.POST.get('texto3')
        group = request.POST.get('grupo')
        device_type = request.POST.get('device_type')
        print('device type'+device_type)
        distributor([ip, texto1, texto2, texto3, group, 'no_configured', device_type])
        return redirect('ViewAccessPoints',group_id=group)
    else:
        return render(request, 'add_one_device.html', {'group_name' : group})

def update_device(request, pk):
    device = Devices.objects.get(pk=ObjectId(pk))
    group_name = GroupDevices.objects.get(group_id=device.group_id) 
    print(group_name.group_name)
    status = distributor([device.ipAddress, device.deviceUser, device.devicePassword, device.vendor, group_name.group_name,'up',device.deviceType])
    if status != 1:
        print(pk)
        Devices.objects.filter(pk=ObjectId(pk)).update(status=status)
    return redirect('device-detail',pk)

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


############################
##Funciones ruckus - VSZ ###
############################

def config_new_one(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = list(data.keys())[0]
        ip_list = data[group_name]
        # print(group_name)
        # print(ip_list)
        devices_list = []
        for device in ip_list:
            devices_list.append([device, 'super', 'sp-admin', 'ruckus', group_name,'default','access_point'])
        scan_devices(devices_list)
        # return JsonResponse({'status': 'success', 'group_name': group_name, 'ip_list': ip_list})
        return redirect('setup',group_name)

def to_controller(request, group_id):
    dispositivos = Devices.objects.filter(group__group_name=group_id, state='oncontroller')
    resultados = []
    for dispositivo in dispositivos:
        # print(dispositivo._id)
        dispositivo_dict = {
            'id': dispositivo._id,
            'host_name': dispositivo.deviceName,
            'version': dispositivo.version,
            'mac_address': dispositivo.macAddress,
            'model': dispositivo.model,
            'ip_address': dispositivo.ipAddress,
            'status': dispositivo.status,
            'serial': dispositivo.serialNumber,
            'clientes': dispositivo.clientes, 
            'controllerStatus': dispositivo.controllerStatus, 
            'controller_status': dispositivo.controllerStatus,
        }
        resultados.append(dispositivo_dict)

    contexto = {
        'dispositivos': resultados,
        'group_name': group_id,
    }
    return render(request, 'to_controller.html', contexto)

def config_ap_on_controller(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = list(data.keys())[0]
        device_list = data[group_name]
        devices_list = []
        for device in device_list:
            mac_serial = device.split()
            # print(mac_serial)
            devices_list.append([mac_serial[0], mac_serial[1]])
        put_ap_info_on_vsz(devices_list)
        return JsonResponse({'status': 'success', 'group_name': group_name, 'ip_list': device_list})    

def set_controller(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = list(data.keys())[0]
        ip_list = data[group_name]
        devices_list = []
        for device in ip_list:
            ip_id = device.split()
            _id = ip_id[1]
            ip_address = ip_id[0]
            dispositivo = get_object_or_404(Devices, pk=ObjectId(_id))
            devices_list.append([ip_address, dispositivo.deviceUser, dispositivo.devicePassword, 'ruckus',_id, group_name,'default'])
        # print(devices_list)
        set_ap_controller(devices_list)
        return JsonResponse({'status': 'success', 'group_name': group_name, 'ip_list': ip_list})    
        # return redirect('setup_ap_controller',group_name)

def get_ap_info_from_vsz(request, pk):
    dispositivo = get_object_or_404(Devices, pk=ObjectId(pk))
    mac_address = dispositivo.macAddress
    _id = dispositivo._id
    group_owner = dispositivo.group
    group_name = group_owner.group_name    
    get_device_from_vsz(mac_address=mac_address.strip(), id =_id)
    return redirect('setup_ap_controller',group_id=group_name)    

def get_aps_from_vsz(request):
    devices = aps_from_vsz()
    return JsonResponse({'ok':'ok'})

def setup_single_ap_on_vsz(request, mac):
    response = set_single_ap_on_vsz(mac)
    return HttpResponse(response)

def get_ap_data_from_mac(request, mac):
    device = get_one_ap_from_vsz(mac)
    return JsonResponse({'ok':'ok'})
    # return JsonResponse(device)

def get_vsz_zones(request):
    get_all_vsz_zones()
    return JsonResponse({'ok':'ok'})
    
def get_vsz_groups(request, group):
    vsz = Controllers.objects.filter(group__group_name=group,deviceType=device_type)
    get_all_groups_from_vsz_zones(group)
    return JsonResponse({'ok':'ok'})


def add_new_controller(request, group):
    if request.method == 'POST':
        ip = request.POST.get('ip')
        username = request.POST.get('username')
        password = request.POST.get('password')
        controller_type = request.POST.get('controller_type')
        group_name = GroupDevices.objects.get(group_name=group)
        controller = Controllers.objects.create(
            host=ip,
            username=username,
            password=password,
            vendor=controller_type,
            group=group_name
        )
        return redirect('ViewVsz', group_name=group)
    else:
        return render(request, 'add_controller.html', {'group_name': group})


############################
#Fin Funciones Ruckus - VSZ#
############################

# def uc_connect(request):
#     data = unifi_controller()
#     return HttpResponse(data)

# def mkt_connect(request):
#     data = connect_mikrotik()
#     return HttpResponse(data)

# def read_excel(request):
#     data = _read_excel()
#     return HttpResponse(data)

# def connect_to_ruckus_ap(Request):    
#     print("intentando conectar")
#     connectRuckus('10.9.21.14','n1mbu5','n3tw0rks.')
#     return HttpResponse("ok")