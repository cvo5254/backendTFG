from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from channels.models import Channel
from channels.serializers import ChannelSerializer
from users.models import CustomUser

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

@api_view(['POST'])
def subscribe_to_channel(request):
    if request.method == 'POST':
        channel_id = request.data.get('channel_id')
        user_id = request.data.get('user_id')

        try:
            channel = Channel.objects.get(id=channel_id)
            user = CustomUser.objects.get(id=user_id)
        except Channel.DoesNotExist:
            return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        channel.subscribers.add(user)
        channel.save()

        return Response({'mensaje': 'Usuario suscrito al canal exitosamente'}, status=status.HTTP_200_OK)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def delete_channel(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
        channel.delete()
        return Response({'mensaje': 'Canal eliminado exitosamente'}, status=status.HTTP_200_OK)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def block_channel(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    channel.is_blocked = True

    channel.save()

    serializer = ChannelSerializer(channel)

    return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['PUT'])
def unblock_channel(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    channel.is_blocked = False

    channel.save()

    serializer = ChannelSerializer(channel)

    return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['PUT'])
def edit_channel(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)

        nombre = request.data.get('nombre')

        if nombre is not None:
            channel.nombre = nombre

        channel.save()
        return Response({'mensaje': 'Canal editado exitosamente'}, status=status.HTTP_200_OK)
    except Channel.DoesNotExist:
        return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_channels(request):
    unblocked_channels = Channel.objects.filter(is_blocked=False)
    serializer = ChannelSerializer(unblocked_channels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_subscriptions(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    channels = user.channel_set.filter(is_blocked=False)
    serializer = ChannelSerializer(channels, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_unsubscribed_channels(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    subscribed_channels = user.channel_set.all()
    all_channels = Channel.objects.exclude(id__in=subscribed_channels).filter(is_blocked=False)
    serializer = ChannelSerializer(all_channels, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def unsubscribe_from_channel(request):
    if request.method == 'POST':
        channel_id = request.data.get('channel_id')
        user_id = request.data.get('user_id')

        try:
            channel = Channel.objects.get(id=channel_id)
            user = CustomUser.objects.get(id=user_id)
        except Channel.DoesNotExist:
            return Response({'error': 'El canal no existe'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        channel.subscribers.remove(user)
        channel.save()

        return Response({'mensaje': 'Usuario eliminado como suscriptor del canal exitosamente'}, status=status.HTTP_200_OK)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
