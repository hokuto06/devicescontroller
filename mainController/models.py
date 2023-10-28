import uuid
from django.db import models

class Devices(models.Model):
    _id = models.CharField(max_length=24, primary_key=True, default=uuid.uuid4().hex, editable=False)
    # _id = models.CharField(max_length=24, primary_key=True)
    ipAddress = models.GenericIPAddressField(unique=True)
    userName =  models.CharField(max_length=100)
    controllerStatus = models.CharField(max_length=40) 
    hostName = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    macAddress = models.CharField(max_length=40)
    status = models.IntegerField()