from rest_framework import serializers
from .models import CustomUser, Gestor

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_active', 'is_staff')
        read_only_fields = ('email', 'is_staff')

class GestorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Gestor
        fields = ('usuario', 'direccion', 'telefono', 'es_administrador')
