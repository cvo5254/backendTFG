from django.urls import path
from .views import get_telegram_messages
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter([]),  # Agrega tus enrutamientos de WebSocket aquí si los necesitas
    }
)
