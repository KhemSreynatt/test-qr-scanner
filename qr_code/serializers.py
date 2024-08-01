from .models import NetworkInfo, Attendances
from rest_framework import serializers

class NetworkInfoSerailizer(serializers.ModelSerializer):
    class Meta:
        model=NetworkInfo
        fields = '__all__'

class AttendanceSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Attendances
        fields = '__all__'
