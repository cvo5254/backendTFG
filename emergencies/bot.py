import requests
from django.http import JsonResponse
from .models import Emergency
from datetime import datetime
from django.db.models import Q
from channels.models import Channel

def process_telegram_messages(request):
    try:
        # Hacer una solicitud a la API de Telegram para obtener los mensajes
        url = f"https://api.telegram.org/bot5957844629:AAGk1zjMGoUcGF0SDA6c3T03eKr3JYShwN4/getUpdates"
        response = requests.get(url)
        data = response.json()

        # Procesar los mensajes recibidos
        if data["ok"]:
            messages = data["result"]
            processed_messages = 0
            for message in messages:
                text = message["message"]["text"]
                chat_name = message["message"]["chat"]["title"]
                
                # Verificar si ya existe una instancia de Emergency con la misma descripción
                existing_emergency = Emergency.objects.filter(Q(description=text)).exists()

                # Comprobar si existe un canal con el nombre del chat
                existing_channel = Channel.objects.filter(nombre=chat_name).first()

                # Si el canal no existe se crea un nuevo canal
                if not existing_channel:
                    new_channel = Channel.objects.create(nombre=chat_name)
                    existing_channel = new_channel
                    existing_channel.save()

                if not existing_emergency:
                    # Crear una instancia de tu modelo de emergencia
                    emergency = Emergency()
                    emergency.title = "Alerta"
                    emergency.description = text
                    emergency.report_date = datetime.now()
                    emergency.publish_date = datetime.now()
                    emergency.is_published = True
                    emergency.channel = existing_channel
                    emergency.save()
                    processed_messages += 1

            if processed_messages == 0:
                return JsonResponse({'message': 'No hay mensajes nuevos'}, status=200)
            else:
                return JsonResponse({'message': f'Se procesaron {processed_messages} mensajes'}, status=200)
        
        return JsonResponse({'message': 'No se recibieron mensajes'}, status=200)
    except Exception as e:
        # Registrar el error
        print(f"Error en process_telegram_messages: {str(e)}")
        return JsonResponse({'error': 'Error interno'}, status=500)
