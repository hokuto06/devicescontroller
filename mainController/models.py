import uuid
# from django.db import models
from djongo import models
#from django.contrib.postgres.fields import JSONField
from djongo.models import JSONField

class GroupDevices(models.Model):
    group_id = models.AutoField(primary_key=True)  # El campo group_id se autogenera
    group_name = models.CharField(max_length=255)

class Devices(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    group = models.ForeignKey(GroupDevices, on_delete=models.CASCADE)
    ipAddress = models.GenericIPAddressField()
    deviceUser = models.CharField(max_length=100)
    devicePassword = models.CharField(max_length=100)
    controllerStatus = models.CharField(max_length=40)
    deviceName = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    vendor = models.CharField(max_length=40)
    macAddress = models.CharField(unique=True, max_length=40)
    clientes = JSONField(default=list, null=True, blank=True)
    status = models.IntegerField()
    serialNumber = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    deviceType = models.CharField(max_length=100, default='access_point', null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    uplink = models.CharField(max_length=100, null=True, blank=True)
    interfaces = JSONField(default=list, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generar un nuevo ID grupal si no se proporciona uno
        if not self.group_id:
            self.group_id = uuid.uuid4()
        super().save(*args, **kwargs)

class UploadFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)