from rest_framework import serializers
from .models import GroupDevices, Devices

class GroupDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDevices
        fields = '__all__'

class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = '__all__'
