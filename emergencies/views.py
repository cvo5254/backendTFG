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

@api_view(['POST'])
def emergency_images_upload(request, emergency_id):
    if request.method == 'POST':
        try:
            emergency = Emergency.objects.get(id=emergency_id)
        except Emergency.DoesNotExist:
            return Response({'error': 'La emergencia no existe'}, status=status.HTTP_404_NOT_FOUND)

        photos = request.FILES.getlist('photos')

        for photo in photos:
            # Aquí puedes realizar el procesamiento y almacenamiento de las fotos
            
            # Por ejemplo, guardando la foto en el sistema de archivos
            photo_path = f'media/emergency_photos/{photo.name}'
            with open(photo_path, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)

            # Puedes agregar la ruta de la foto a la lista de fotos asociadas a la emergencia
            emergency.photos.add(photo_path)

        emergency.save()

        serializer = EmergencySerializer(emergency)

        return Response({'mensaje': 'Fotos subidas exitosamente', 'emergencia': serializer.data}, status=status.HTTP_200_OK)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_emergencies(request):
    # Obtener todas las emergencias
    emergencias = Emergency.objects.all()

    # Obtener el valor del parámetro opcional "is_published"
    is_published = request.query_params.get('is_published')

    # Si el parámetro is_published tiene valor, filtrar por ese valor
    if is_published is not None:
        emergencias = emergencias.filter(is_published=is_published)

    # Serializar las emergencias y devolver la respuesta
    serializer = EmergencySerializer(emergencias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_emergency(request, emergency_id):
    try:
        emergency= Emergency.objects.get(id=emergency_id)
        serializer = EmergencySerializer(emergency)
        return Response(serializer.data)
    except Emergency.DoesNotExist:
        return Response({'error': 'La emergencia no existe'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_emergency(request, id):
    try:
        emergencia = Emergency.objects.get(id=id)
        emergencia.delete()
        return Response({'mensaje': 'Emergencia eliminada exitosamente'}, status=status.HTTP_200_OK)
    except Emergency.DoesNotExist:
        return Response({'error': 'La emergencia no existe'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def edit_emergency(request, id):
    try:
        emergencia = Emergency.objects.get(id=id)

        title = request.data.get('title')
        description = request.data.get('description')
        channel_id = request.data.get('channel_id')
        is_published = request.data.get('is_published')
        images = request.data.get('images')

        if title is not None:
            emergencia.title = title
        if description is not None:
            emergencia.description = description
        if channel_id is not None:
            channel = Channel.objects.get(id=channel_id)
            emergencia.channel = channel
        if is_published is not None:
            emergencia.is_published = is_published
        if images is not None:
            emergencia.images = images

        emergencia.save()
        return Response({'mensaje': 'Emergencia editada exitosamente'}, status=status.HTTP_200_OK)
    except Emergency.DoesNotExist:
        return Response({'error': 'La emergencia no existe'}, status=status.HTTP_404_NOT_FOUND)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
