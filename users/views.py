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

        # Validar si la contraseña es correcta
        if usuario.check_password(password):
            # Realizar la lógica de inicio de sesión para el usuario básico
            # ...

            # Devolver la respuesta de éxito
            return Response({'mensaje': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
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
            return Response({'mensaje': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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

