from rest_framework import serializers
from .models import Channel

class ChannelSerializer(serializers.ModelSerializer):
    subscribers = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Channel
        fields = ['id', 'nombre', 'subscribers']
