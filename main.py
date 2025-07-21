from flask import Flask, request
import telebot
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import os

API_TOKEN = '7590984094:AAGuVH13k26Iynyz-BATElSTMiyT3Y7LtB8'  # ТВОЙ ТОКЕН
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Music bot is running 24/7'

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎵 Привет! Просто отправь мне название песни или ссылку (YouTube, TikTok, Instagram) — я скачаю музыку 🎧")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    query = message.text.strip()

    # Проверка: это ссылка или название?
    if query.startswith("http"):
        url = query
    else:
        # Поиск на YouTube по названию
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()
        if not result['result']:
            bot.reply_to(message, "❌ Ничего не найдено.")
            return
        url = result['result'][0]['link']

    msg = bot.reply_to(message, "⏬ Загружаю музыку, подожди немного...")

    # Скачивание с помощью yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_song.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Аудио')
            performer = info.get('uploader', 'Unknown')
            duration = info.get('duration', 0)
        
        audio = open("downloaded_song.mp3", "rb")
        bot.send_audio(
            message.chat.id, 
            audio, 
            title=title,
            performer=performer,
            duration=duration
        )
        audio.close()
        os.remove("downloaded_song.mp3")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при скачивании:\n{str(e)}")
        print("Ошибка:", e)

# Установка webhook (для Replit или Railway)
import telebot.util
import threading

WEBHOOK_URL = f"https://{os.environ.get('REPL_SLUG')}.{os.environ.get('REPL_OWNER')}.repl.co/{API_TOKEN}"

def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

threading.Thread(target=set_webhook).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
