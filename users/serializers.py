from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Gestor

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

class GestorSerializer(UserSerializer):
    direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=20)
    es_administrador = serializers.BooleanField()

    class Meta(UserSerializer.Meta):
        model = Gestor
        fields = UserSerializer.Meta.fields + ['direccion', 'telefono', 'es_administrador']

    def create(self, validated_data):
        gestor = Gestor.objects.create_user(**validated_data)
        gestor.direccion = validated_data.get('direccion')
        gestor.telefono = validated_data.get('telefono')
        gestor.es_administrador = validated_data.get('es_administrador')
        gestor.save()
        return gestor

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.es_administrador = validated_data.get('es_administrador', instance.es_administrador)
        instance.save()
        return instance
