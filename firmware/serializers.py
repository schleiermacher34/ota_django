# your_existing_app/serializers.py

from rest_framework import serializers
from .models import MachineLog

class MachineLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineLog
        fields = '__all__'
