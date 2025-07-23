from flask import Flask, request
import telebot

TOKEN = '7794349596:AAEVqwZXfRD5QD-ibSuHgU9XeKnd5Dc6HS8'  # Замени на нужный токен, если он другой
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Ответ на команду /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "✅ Бот работает!")

# Обработка обновлений Telegram
@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Установка webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    url = f"https://{request.host}/{TOKEN}"
    bot.remove_webhook()
    result = bot.set_webhook(url=url)
    return "Webhook установлен ✅" if result else "Ошибка ❌"

# Запуск Flask-сервера
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
