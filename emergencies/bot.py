import requests
from django.http import JsonResponse
from .models import Emergency
from datetime import datetime

def process_telegram_messages(request):
    try:
        # Hacer una solicitud a la API de Telegram para obtener los mensajes
        url = f"https://api.telegram.org/bot5957844629:AAGk1zjMGoUcGF0SDA6c3T03eKr3JYShwN4/getUpdates"
        response = requests.get(url)
        data = response.json()

        # Procesar los mensajes recibidos
        if data["ok"]:
            messages = data["result"]
            for message in messages:
                chat_id = message["message"]["chat"]["id"]
                text = message["message"]["text"]

                # Realizar las acciones que deseas con los datos del mensaje
                # Por ejemplo, crear una instancia de tu modelo de emergencia
                emergency = Emergency()
                emergency.title = "Alerta"
                emergency.description = text
                emergency.report_date = datetime.now()
                emergency.publish_date = datetime.now()
                emergency.is_published = True
                emergency.save()

        return JsonResponse({'message': 'Mensajes procesados'}, status=200)
    except Exception as e:
        # Registrar el error
        print(f"Error en process_telegram_messages: {str(e)}")
        return JsonResponse({'error': 'Error interno'}, status=500)
