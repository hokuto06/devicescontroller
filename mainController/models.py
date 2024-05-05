import uuid
from django.db import models
#from django.contrib.postgres.fields import JSONField
from djongo.models import JSONField


class GroupDevices(models.Model):
    group_id = models.AutoField(primary_key=True)  # El campo group_id se autogenera
    group_name = models.CharField(max_length=255)

class Devices(models.Model):
    # _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    _id = models.CharField(primary_key=True, max_length=24)
    # _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # _id = models.AutoField(primary_key=True)
    # _id = models.CharField(max_length=24, primary_key=True, default=uuid.uuid4().hex, editable=False)
    # group_id = models.UUIDField(default=uuid.uuid4, editable=False)  # Campo para el ID grupal
    # group_id = models.ReferenceField(GroupDevices, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupDevices, on_delete=models.CASCADE)
    ipAddress = models.GenericIPAddressField(unique=True)
    deviceUser = models.CharField(max_length=100)
    devicePassword = models.CharField(max_length=100)
    controllerStatus = models.CharField(max_length=40)
    deviceName = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    macAddress = models.CharField(max_length=40)
    clientes = JSONField(default=list, null=True, blank=True)
    status = models.IntegerField()

    def save(self, *args, **kwargs):
        # Generar un nuevo ID grupal si no se proporciona uno
        if not self.group_id:
            self.group_id = uuid.uuid4()
        super().save(*args, **kwargs)
