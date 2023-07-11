import telebot
import youtube_dl
import os

bot = telebot.TeleBot("5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a YouTube video URL and I'll download it for you in the highest quality available.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', None)
        video_ext = info_dict.get('ext', None)
        video_filename = f"{video_title}.{video_ext}"
    video = open(video_filename, 'rb')
    bot.send_video(message.chat.id, video)
    video.close()
    os.remove(video_filename)

bot.polling()
