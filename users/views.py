from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer, GestorSerializer
from .models import CustomUser, Gestor

@api_view(['POST'])
def login_desde_movil(request):
    # Validar que se esté haciendo una petición POST
    if request.method == 'POST':
        # Obtener los datos de inicio de sesión desde la petición
        email = request.data.get('email')
        password = request.data.get('password')

        # Validar si el usuario es básico
        try:
            usuario = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario está activo
        if not usuario.is_active:
            return Response({'error': 'El usuario está inactivo'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si el usuario está bloqueado
        if usuario.is_blocked:
            return Response({'error': 'El usuario está bloqueado'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar si la contraseña es correcta
        if usuario.check_password(password):
            # Realizar la lógica de inicio de sesión para el usuario básico
            # ...

            usuario_serializer = UsuarioSerializer(usuario)  # Importa el serializador correspondiente
            return Response({'mensaje': 'Inicio de sesión exitoso', 'usuario': usuario_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def login_desde_web(request):
    # Validar que se esté haciendo una petición POST
    if request.method == 'POST':
        # Obtener los datos de inicio de sesión desde la petición
        email = request.data.get('email')
        password = request.data.get('password')

        # Validar si el usuario es gestor
        try:
            gestor = Gestor.objects.get(email=email)
        except Gestor.DoesNotExist:
            return Response({'error': 'El gestor no existe'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar si la contraseña es correcta
        if gestor.check_password(password):
            # Realizar la lógica de inicio de sesión para el gestor
            # ...

            # Devolver la respuesta de éxito
            gestor_serializer = GestorSerializer(gestor)
            return Response({'mensaje': 'Inicio de sesión exitoso', 'gestor': gestor_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_gestor(request):
    email = request.data.get('email')
    password = request.data.get('password')
    direccion = request.data.get('direccion')
    telefono = request.data.get('telefono')
    es_administrador = request.data.get('es_administrador')

    try:
        gestor = Gestor.objects.create_user(email=email, password=password)
        gestor.direccion = direccion
        gestor.telefono = telefono
        gestor.es_administrador = es_administrador
        gestor.save()
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = GestorSerializer(gestor)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def registro_usuario(request):
    # Validar que se esté haciendo una petición POST
    if request.method == 'POST':
        # Obtener los datos de registro desde la petición
        email = request.data.get('email')
        password = request.data.get('password')
        # Puedes agregar más campos necesarios para el registro
        try:
            usuario = CustomUser.objects.create_user(email=email, password=password)
            # Puedes agregar más campos necesarios para el registro
            usuario.save()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serializar el usuario creado
        serializer = UsuarioSerializer(usuario)

        # Devolver la respuesta de éxito
        return Response({'mensaje': 'Registro de usuario exitoso', 'usuario': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PUT'])
def activar_usuario(request):
    # Validar que se esté haciendo una petición PUT
    if request.method == 'PUT':
        # Obtener el ID del usuario a activar desde la petición
        user_id = request.data.get('user_id')
        
        # Buscar el usuario a activar
        try:
            usuario = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Activar el usuario
        usuario.is_active = True
        usuario.save()

        # Serializar el usuario modificado
        serializer = UsuarioSerializer(usuario)

        # Devolver la respuesta de éxito
        return Response({'mensaje': 'Activación de usuario exitosa', 'usuario': serializer.data}, status=status.HTTP_200_OK)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def obtener_usuarios_basicos(request):
    # Obtener los usuarios básicos (no gestores)
    usuarios_basicos = CustomUser.objects.exclude(gestor__isnull=False)
    

    # Obtener el valor del parámetro opcional "is_active"
    is_active = request.query_params.get('is_active')

    # Si el parámetro is_active tiene valor, filtrar por ese valor
    if is_active is not None:
        usuarios_basicos = usuarios_basicos.filter(is_active=is_active)

    # Serializar los usuarios y devolver la respuesta
    serializer = UsuarioSerializer(usuarios_basicos, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        return Response({'mensaje': 'Usuario eliminado exitosamente'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def block_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    user.is_blocked = True

    user.save()

    serializer = UsuarioSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['PUT'])
def unblock_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
    
    user.is_blocked = False

    user.save()

    serializer = UsuarioSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)
