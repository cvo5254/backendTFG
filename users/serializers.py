from rest_framework import serializers
from .models import CustomUser, Gestor

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'is_active', 'is_staff')
        read_only_fields = ('email', 'is_staff')

class GestorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gestor
        fields = ('id', 'email', 'es_administrador')
