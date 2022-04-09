from .models import IdInfo
from rest_framework import serializers


class IdInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdInfo
        fields = ['id', 'first_name', 'last_name', 'position',
                  'emergency_contact_name', 'contact_number', 'address', 'image']
