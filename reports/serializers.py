from rest_framework import serializers
from .models import Vunerabilities

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vunerabilities
        fields = '__all__'


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vunerabilities
        fields = '__all__'
        extra_kwargs = {'fixed': {'required': True},'hostname': {'required': False},'ip_address': {'required': False},'title': {'required': False},'severity': {'required': False}}

    def update(self,instance,validated_data):
        instance.fixed = validated_data.get('fixed',instance.fixed)
        instance.save()

        return instance