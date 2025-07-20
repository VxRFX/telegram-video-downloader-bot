import telebot
import yt_dlp
import os

TOKEN = '7794349596:AAEVqwZXfRD5QD-ibSuHgU9XeKnd5Dc6HS8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Привет! Отправь мне ссылку на видео из TikTok, Instagram или YouTube.")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text

    bot.send_chat_action(message.chat.id, 'upload_video')
    bot.send_message(message.chat.id, "🔄 Загружаю видео...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "retries": 1,
        "concurrent_fragment_downloads": 4,
        "fragment_retries": 1
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = None
        for file in os.listdir():
            if file.startswith("video") and file.endswith(".mp4"):
                video_file = file
                break

        if video_file:
            with open(video_file, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(video_file)
        else:
            bot.send_message(message.chat.id, "⚠ Видео не найдено. Попробуй другую ссылку.")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")

bot.polling()
