"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import login_desde_web, login_desde_movil, registro_usuario, activar_usuario, obtener_usuarios_basicos
from channels.views import create_channel, subscribe_to_channel, get_user_subscriptions, get_unsubscribed_channels, unsubscribe_from_channel
from emergencies.views import create_emergency, get_channel_emergencies, publish_emergency, emergency_images_upload, get_emergencies

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_desde_web, name='login'),
    path('api/login_movil/', login_desde_movil, name='login_movil'),
    path('api/registro/', registro_usuario, name='registro_usuario'),
    path('api/aprobar_registro', activar_usuario, name='activar_usuario'),
    path('api/obtener_usuarios/', obtener_usuarios_basicos, name='obtener_usuarios'),
    path('api/crear_canal/', create_channel, name='crear_canal'),
    path('api/crear_emergencia/', create_emergency, name='crear_emergencia'),
    path('api/suscribirse/', subscribe_to_channel, name='suscribirse_a_canal'),
    path('api/<int:user_id>/subscriptions/', get_user_subscriptions,  name='user_subscriptions'),
    path('api/<int:user_id>/notSuscribedChannels/', get_unsubscribed_channels, name = 'obtener_canales_no_suscritos'),
    path('api/<int:channel_id>/emergencies', get_channel_emergencies, name='emergencias del canal'),
    path('api/<int:emergency_id>/publish', publish_emergency, name='publicar emergencia'),
    path('api/<int:emergency_id>/upload/', emergency_images_upload, name='publicar fotos de emergencias'),
    path('api/unsuscribe/', unsubscribe_from_channel, name='desuscribirse de canal'),
    path('api/allemergencies/', get_emergencies, name='obtener emergencias')
]