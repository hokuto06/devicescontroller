from django.contrib import admin
from mainController import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  views.inicio, name="Inicio"),
    path('table', views.table, name="Table"),
    path('test', views.test, name="Test"),
    path('view-devices', views.view_devices),
]