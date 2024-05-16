from django.contrib import admin
from mainController import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.inicio, name="Inicio"),
    #path('table', views.table, name="Table"),
    path('test', views.read_excel, name="Test"),
    # path('ruckus', views.connect_to_ruckus_ap, name="Rucus"),
    path('uc', views.uc_connect, name="uc"),
    path('mkt', views.mkt_connect, name="mkt"),
    path('view-devices/<str:group_id>', views.view_access_points, name="ViewAccessPoints"),
    path('view-gateway/<str:group_id>', views.view_gateway, name="ViewGateway"),
    path('delete-all', views.delete_all),
    path('crear_grupo/', views.crear_grupo, name='CrearGrupo'),
    path('add_one_device/<str:group>/', views.add_one, name='add_one_device'),
    path('procesar_formulario/<str:group>/', views.procesar_formulario, name='procesar_formulario'),
    path('group/<str:group>', views.view_group),
    path('config-new-one/>', views.config_new_one, name="config-new-one"),
    path('delete-device/<pk>', views.delete_device, name='DeleteDevice'),
    # path('devices/', views.DevicesListCreateView.as_view(), name='devices-list-create'),
    path('devices/<int:group>/', views.DevicesListCreateView.as_view(), name='devices-list-create-filtered'),
    # path('devices/<str:pk>/', views.DevicesDetailView.as_view(), name='devices-detail'),
    path('groups/', views.GroupDevicesListCreateView.as_view(), name='group-devices-list-create'),
    path('devices-test/', views.devices_api, name='devices_api'),
    # path('device/<str:ipAddress>/', views.device_detail, name='device_detail'),
    path('device/<pk>/', views.device_detail_view, name='device-detail'),
    path('update_device/<pk>/', views.update_device, name='update_device'),
    # path('viewdevice/<str:pk>/', views.DevicesDetailView.as_view(), name='view-device-detail'),
    path('viewdevice/', views.DevicesDetailView.as_view(), name='view-device-detail'),
]