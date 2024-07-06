from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from accounts.models import CompanyUser

class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

class CompanyUserSerializer(serializers.Serializer):
    id = ObjectIdField(read_only=True)
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = CompanyUser(**validated_data)
        user.save()
        return user