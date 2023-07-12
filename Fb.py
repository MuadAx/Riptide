import http.client
import telebot
import requests
import json
import os
from moviepy.editor import VideoFileClip

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "مرحبا! يرجى إرسال رابط الفيديو الذي ترغب في تنزيله.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    conn = http.client.HTTPSConnection("facebook-reel-and-video-downloader.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': "a0991caeb2msh9fe32fe43098915p1dcc21jsn5cdf0de856df",
        'X-RapidAPI-Host': "facebook-reel-and-video-downloader.p.rapidapi.com"
    }
    conn.request("GET", f"/app/main.php?url={url}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    video_url = data.decode("utf-8")

    # Parse JSON string
    data = json.loads(video_url)

    # Extract video URL
    if 'Download High Quality' in data['links']:
        video_url = data['links']['Download High Quality']
    else:
        video_url = data['links']['Download Low Quality']

    # Download video file
    response = requests.get(video_url, timeout=30) # Set timeout to 30 seconds
    video_file = open('video.mp4', 'wb')
    video_file.write(response.content)
    video_file.close()

    # Get file size
    file_size = os.path.getsize('video.mp4')
    file_size = round(file_size / (1024 * 1024), 2)

    # Get video duration
    clip = VideoFileClip('video.mp4')
    duration = round(clip.duration / 60, 2)

    # Send video info
    bot.send_message(message.chat.id, f'حجم الملف: {file_size} ميغابايت\nمدة الفيديو: {duration} دقيقة')

bot.polling()
