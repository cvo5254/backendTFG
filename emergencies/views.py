from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from emergencies.models import Emergency
from emergencies.serializers import EmergencySerializer
from users.models import CustomUser

@api_view(['POST'])
def create_emergency(request):
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('decriprio')
        channel = request.data.get('channel_id')
        reporter_id = request.data.get('reporter_id')
        report_date = datetime.now()

        try:
            emergency = Emergency.objects.create(title=title, description=description, channel=channel, reporter_id=reporter_id, report_date=report_date)
            emergency.save()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmergencySerializer(emergency)

        return Response({'mensaje': 'Emergencia creada exitosamente', 'canal': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
