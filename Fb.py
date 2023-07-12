import http.client
import telebot
import requests
import json
import os

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! Please send the Facebook video URL you want to download.")

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
    response = requests.get(video_url, timeout=1030) # Set timeout to 30 seconds
    video_file = open('video.mp4', 'wb')
    video_file.write(response.content)
    video_file.close()

    # Check file size
    file_size = os.path.getsize('video.mp4')
    max_size = 50 * 1024 * 1024  # 50 MB
    if file_size > max_size:
        # Split the file into parts
        os.popen(f'split -b {max_size} video.mp4 video.part.')
        # Send each part
        part_number = 1
        for part in sorted(os.listdir('.')):
            if part.startswith('video.part.'):
                with open(part, 'rb') as f:
                    bot.send_document(message.chat.id, f, caption=f'Part {part_number}')
                os.remove(part)
                part_number += 1
    else:
        # Send the file
        with open('video.mp4', 'rb') as f:
            bot.send_document(message.chat.id, f)

bot.polling()
