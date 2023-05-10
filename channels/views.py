from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from channels.models import Channel
from channels.serializers import ChannelSerializer

@api_view(['POST'])
def create_channel(request):
    if request.method == 'POST':
        nombre = request.data.get('nombre')


        try:
            channel = Channel.objects.create(nombre=nombre)
            channel.save()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ChannelSerializer(channel)

        return Response({'mensaje': 'Canal creado exitosamente', 'canal': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
