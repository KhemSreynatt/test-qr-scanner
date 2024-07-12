from .models import NetworkGPS, Attendances
from rest_framework import serializers

class NetworkGPSSerailizer(serializers.ModelSerializer):
    class Meta:
        model=NetworkGPS
        fields = '__all__'

class AttendanceSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Attendances
        fields = '__all__'
