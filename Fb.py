import http.client
import telebot
import requests
import json
import os
import subprocess


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
        # Re-encode the video using a lower bitrate
        subprocess.call('ffmpeg -i video.mp4 -b:v 1M -c:a copy output.mp4 -y', shell=True)
        os.rename('output.mp4', 'video.mp4')

        # Send status update
        bot.send_message(message.chat.id, "The video file has been re-encoded to reduce its size.")


    # Send the file as a video
    with open('video.mp4', 'rb') as f:
        bot.send_video(message.chat.id, f)


    # Send final status update
    bot.send_message(message.chat.id, "Upload complete!")


bot.polling()
