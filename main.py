from flask import Flask, request
import telebot

TOKEN = '7794349596:AAEVqwZXfRD5QD-ibSuHgU9XeKnd5Dc6HS8'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Обработка команд
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот для скачивания видео.")

# Вебхук для Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Установка вебхука
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    webhook_url = f'https://5af00bb5-9b24-4d2e-95a6-ebed7df1c5ef-00-3c7mkuuweanq4.sisko.replit.dev/{TOKEN}'
    bot.remove_webhook()
    success = bot.set_webhook(url=webhook_url)
    return 'Установлено' if success else 'Ошибка'

# Запуск Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
