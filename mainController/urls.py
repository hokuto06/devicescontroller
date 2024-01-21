from django.contrib import admin
from mainController import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.inicio, name="Inicio"),
    #path('table', views.table, name="Table"),
    path('test', views.test, name="Test"),
    path('view-devices/<str:group_id>', views.view_access_points, name="ViewAccessPoints"),
    path('delete-all', views.delete_all),
    path('crear_grupo/', views.crear_grupo, name='CrearGrupo'),
    path('procesar_formulario/<str:group>/', views.procesar_formulario, name='procesar_formulario'),
    path('group/<str:group>', views.view_group),
    path('delete-device/<str:device_id>', views.delete_device, name='DeleteDevice'),
    # path('devices/', views.DevicesListCreateView.as_view(), name='devices-list-create'),
    path('devices/<int:group>/', views.DevicesListCreateView.as_view(), name='devices-list-create-filtered'),
    # path('devices/<str:pk>/', views.DevicesDetailView.as_view(), name='devices-detail'),
    path('groups/', views.GroupDevicesListCreateView.as_view(), name='group-devices-list-create'),
    path('devices-test/', views.devices_api, name='devices_api'),
    # path('device/<str:ipAddress>/', views.device_detail, name='device_detail'),
    path('device/<uuid:pk>/', views.device_detail_view, name='device-detail'),
    path('viewdevice/<uuid:pk>/', views.DevicesDetailView.as_view(), name='view-device-detail'),
]