from rest_framework import serializers
from .models import Emergency
from channels.serializers import ChannelSerializer
from users.serializers import CustomUserSerializer

class EmergencySerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    reporter = CustomUserSerializer()

    class Meta:
        model = Emergency
        fields = ['id', 'title', 'description', 'report_date', 'publish_date', 'channel', 'reporter']
