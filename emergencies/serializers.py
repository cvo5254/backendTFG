from rest_framework import serializers
from .models import Emergency
from channels.serializers import ChannelSerializer
from users.serializers import UsuarioSerializer
import base64

class EmergencySerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    reporter = UsuarioSerializer()
    images = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Emergency
        fields = ['id', 'title', 'description', 'report_date', 'publish_date', 'channel', 'reporter', 'is_published', 'images']


class EmergencyListSerializer(serializers.ModelSerializer):
    images = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Emergency
        fields = ['id', 'title', 'description', 'images']

    def get_images(self, obj):
        if obj.images:
            try:
                with open(obj.images.path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                    return encoded_image
            except FileNotFoundError:
                return None
        return None

    
        