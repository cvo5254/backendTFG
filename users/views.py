from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and not user.is_gestor:
            login(request, user)
            return JsonResponse({'success': True})
        elif user is not None and user.is_gestor:
            return JsonResponse({'error': 'Este usuario no está autorizado para iniciar sesión.'})
        else:
            return JsonResponse({'error': 'Credenciales inválidas.'})

    return JsonResponse({'error': 'Método no permitido.'})