from telegram import Bot

# Crear una instancia de tu bot
bot = Bot(token='5957844629:AAGk1zjMGoUcGF0SDA6c3T03eKr3JYShwN4')

def get_updates():
    try:
        # Obtener las actualizaciones (mensajes) más recientes del grupo
        updates =  bot.get_updates()
        print(updates)
        
        for update in updates:
             process_update(update)
    except Exception as e:
        # Registrar el error
        print(f"Error en get_updates: {str(e)}")

def process_update(update):
    try:
        # Aquí puedes manejar la actualización recibida
        message = update.message
        chat_id = message.chat_id
        text = message.text
        
        # Realiza las acciones que deseas con los datos del mensaje
        # Por ejemplo, crear una instancia de tu modelo de emergencia
        emergency = Emergency()
        emergency.title = "Alerta"
        emergency.description = text
        emergency.report_date = timezone.now()
        emergency.publish_date = timezone.now()
        emergency.is_published = True
        emergency.save()
    except Exception as e:
        # Registrar el error
        print(f"Error en process_update: {str(e)}")
