from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from emergencies.models import Emergency
from emergencies.serializers import EmergencySerializer
from emergencies.serializers import EmergencyListSerializer
from users.models import CustomUser
from channels.models import Channel

@api_view(['POST'])
def create_emergency(request):
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        channel_id = request.data.get('channel_id')
        reporter_id = request.data.get('reporter_id')
        report_date = datetime.now()

        try:
            channel = Channel.objects.get(id=channel_id)
            emergency = Emergency.objects.create(title=title, description=description, channel=channel, reporter_id=reporter_id, report_date=report_date)
            emergency.save()
        except Channel.DoesNotExist:
            return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmergencySerializer(emergency)

        return Response({'mensaje': 'Emergencia creada exitosamente', 'emergencia': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(['GET'])
def get_channel_emergencies(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)

    emergencies = Emergency.objects.filter(channel=channel, is_published=True)
    serializer = EmergencyListSerializer(emergencies, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def publish_emergency(request, emergency_id):
    try:
        emergency = Emergency.objects.get(id=emergency_id)
    except Emergency.DoesNotExist:
        return Response({'error': 'La emergencia no existe'}, status=status.HTTP_404_NOT_FOUND)

    emergency.publish_date = datetime.now()
    emergency.is_published = True

    channel_id = request.data.get('channel_id')
    if channel_id:
        try:
            channel = Channel.objects.get(id=channel_id)
            emergency.channel = channel
        except Channel.DoesNotExist:
            return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)

    emergency.save()

    serializer = EmergencySerializer(emergency)

    return Response(serializer.data, status=status.HTTP_200_OK)
