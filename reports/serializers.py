from rest_framework import serializers
from .models import Vunerabilities

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vunerabilities
        fields = '__all__'