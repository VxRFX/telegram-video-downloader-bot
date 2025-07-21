import telebot
from flask import Flask, request
import yt_dlp
import os

BOT_TOKEN = 'ТВОЙ_ТОКЕН'  # замени на свой токен
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# обработка команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Отправь ссылку на видео из YouTube, TikTok или Instagram.")

# обработка всех сообщений
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
        bot.send_message(message.chat.id, f"❌ Ошибка при скачивании:\n{e}")

# webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

# запуск сервера
@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co/{BOT_TOKEN}")
    app.run(host="0.0.0.0", port=3000)
