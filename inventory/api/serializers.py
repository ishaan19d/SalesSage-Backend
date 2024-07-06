# serializers.py
from rest_framework import serializers
from inventory.models import Items

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

    def to_representation(self, instance):
        return {key: value for key, value in instance.__dict__.items() if not key.startswith('_')}

    def to_internal_value(self, data):
        return data