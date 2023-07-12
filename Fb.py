import os
import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ['telebot', 'imageio', 'http.client', 'requests', 'json', 'os', 'Pillow']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

import http.client
import telebot
import requests
import json
import os
import imageio
from PIL import Image

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

    # Send status update
    status_message = bot.send_message(message.chat.id, "Now downloading video...")

    # Download video file
    response = requests.get(video_url, timeout=1030) # Set timeout to 30 seconds
    video_file = open('video.mp4', 'wb')
    video_file.write(response.content)
    video_file.close()

    # Send file size
    file_size = os.path.getsize('video.mp4')
    bot.send_message(message.chat.id, f"The downloaded file size is {file_size / (1024 * 1024):.2f} MB.")

    # Check file size
    max_size = 50 * 1024 * 1024  # 50 MB
    if file_size > max_size:
        # Calculate the number of parts
        parts = (file_size + max_size - 1) // max_size

        # Extract thumbnail from the original video
        reader = imageio.get_reader('video.mp4')
        frame = reader.get_data(0)
        image = Image.fromarray(frame)
        image = image.convert('RGB')
        image.save('thumbnail.jpg')

        # Split the file into parts
        with open('video.mp4', 'rb') as f:
            data = f.read()
            part_size = len(data) // parts
            part_number = 1
            start = 0
            while start < len(data):
                end = min(start + part_size, len(data))
                part = data[start:end]
                with open(f'part{part_number}.mp4', 'wb') as f:
                    f.write(part)
                start += part_size;
                part_number += 1

        # Send status update
        bot.send_message(message.chat.id, "Now uploading to Telegram...")

        # Send each part
        part_number = 1;
        for part in sorted(os.listdir('.')):
            if part.startswith('part'):
                with open(part, 'rb') as f:
                    bot.send_video(message.chat.id, f, thumb='thumbnail.jpg', caption=f'Part {part_number}')
                os.remove(part)
                part_number += 1

        # Send final status update
        bot.send_message(message.chat.id, "Upload complete!")
    elif file_size > 0:
        # Extract thumbnail from the original video
        reader = imageio.get_reader('video.mp4')
        frame = reader.get_data(0)
        image = Image.fromarray(frame)
        image = image.convert('RGB')
        image.save('thumbnail.jpg')

        # Send the file
        with open('video.mp4', 'rb') as f:
            bot.send_video(message.chat.id, f, thumb='thumbnail.jpg')

        # Send final status update
        bot.send_message(message.chat.id, "Upload complete!")
    else:
        bot.send_message(message.chat.id, "The downloaded file is empty. Please check the URL and try again.")

bot.polling()
