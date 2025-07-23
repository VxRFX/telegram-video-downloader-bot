import telebot
from flask import Flask, request
import yt_dlp
import os

BOT_TOKEN = "7794349596:AAEVqwZXfRD5QD-ibSuHgU9XeKnd5Dc6HS8"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "🎥 Привет! Отправь ссылку на видео с YouTube, TikTok или Instagram.")

# обработка ссылок
@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏬ Скачиваю видео, подожди...")
    try:
        with yt_dlp.YoutubeDL({'outtmpl': 'video.%(ext)s'}) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        os.remove(filename)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# --- ВАЖНО: маршрут установки webhook ---
@app.route('/set_webhook', methods=["GET"])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://5af00bb5-9b24-4d2e-95a6-ebed7df1c5ef-00-3c7mkuuweanq4.sisko.replit.dev/' + BOT_TOKEN)
    return "Webhook установлен"

# webhook
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
