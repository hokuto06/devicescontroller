from django.shortcuts import render
from django.http import HttpResponse
from .models import Devices
from .controller import main

def inicio(req):

    return render(req, 'base.html')

def table(req):
    
    return render(req, 'table.html')

def test(req):
    resultado = main()
    # Haz algo con el resultado, por ejemplo, retornarlo como una respuesta HTTP
    return HttpResponse(resultado)    

def view_devices(request):
    # Recupera todos los objetos Devices de la base de datos
    dispositivos = Devices.objects.all()

    # Crea una lista de diccionarios para almacenar los resultados
    resultados = []
    for dispositivo in dispositivos:
        # Agrega los atributos relevantes del objeto a un diccionario
        dispositivo_dict = {
            'id': dispositivo.ipAddress,
            'version': dispositivo.version,
            'mac_address': dispositivo.macAddress,
            'model': dispositivo.model,
            'ip_address': dispositivo.ipAddress,
            'status': dispositivo.status,
            'controller_status': dispositivo.controllerStatus,
        }
        resultados.append(dispositivo_dict)

    # Crea un diccionario de contexto con la lista de dispositivos
    contexto = {
        'dispositivos': resultados,
    }

    # Renderiza el template con el diccionario de contexto y retorna la respuesta HTTP
    return render(request, 'table.html', contexto)
