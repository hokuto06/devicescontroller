from django.contrib import admin
from mainController import views
from django.conf import settings
from django.conf.urls.static import static
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
    path('config-new-one/', views.config_new_one, name="config-new-one"),
    path('get-ap-info-from-vsz/<pk>', views.get_ap_info_from_vsz, name='GetApInfoFromVsz'),
    path('delete-device/<pk>', views.delete_device, name='DeleteDevice'),
    # path('devices/', views.DevicesListCreateView.as_view(), name='devices-list-create'),
    path('devices/<int:group>/', views.DevicesListCreateView.as_view(), name='devices-list-create-filtered'),
    # path('devices/<str:pk>/', views.DevicesDetailView.as_view(), name='devices-detail'),
    path('groups/', views.GroupDevicesListCreateView.as_view(), name='group-devices-list-create'),
    path('devices-test/', views.devices_api, name='devices_api'),
    # path('device/<str:ipAddress>/', views.device_detail, name='device_detail'),
    path('device/<pk>/', views.device_detail_view, name='device-detail'),
    path('update_device/<pk>/', views.update_device, name='update_device'),
    path('setup/<str:group_id>', views.setup_devices, name='setup' ),
    path('setup_ap_controller/<str:group_id>', views.to_controller, name='setup_ap_controller' ),
    path('config_on_controller/', views.config_ap_on_controller, name='config-on-controller' ),
    path('set_controller/', views.set_controller, name='set-controller' ),
    # path('viewdevice/<str:pk>/', views.DevicesDetailView.as_view(), name='view-device-detail'),
    #path('upload/', views.upload_file, name='upload_file'),
    path('upload/<str:group_id>/', views.upload_file, name='upload_file'),
    path('viewdevice/', views.DevicesDetailView.as_view(), name='view-device-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)