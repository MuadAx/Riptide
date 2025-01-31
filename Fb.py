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
        # Calculate the number of parts
        parts = (file_size + max_size - 1) // max_size


        # Split the file into parts using ffmpeg
        duration = float(subprocess.check_output(f'ffprobe -i video.mp4 -show_entries format=duration -v quiet -of csv="p=0"', shell=True))
        part_duration = duration / parts
        for part_number in range(parts):
            start = part_number * part_duration
            end = start + part_duration
            subprocess.call(f'ffmpeg -ss {start} -i video.mp4 -t {part_duration} -c copy part{part_number + 1}.mp4 -y', shell=True)


        # Send status update
        bot.send_message(message.chat.id, "Now uploading to Telegram...")


        # Send each part
        part_number = 1
        for part in sorted(os.listdir('.')):
            if part.startswith('part'):
                with open(part, 'rb') as f:
                    bot.send_video(message.chat.id, f, caption=f'Part {part_number}')
                os.remove(part)
                part_number += 1


        # Send final status update
        bot.send_message(message.chat.id, "Upload complete!")
    elif file_size > 0:
        # Send the file
        with open('video.mp4', 'rb') as f:
            bot.send_video(message.chat.id, f)


        # Send final status update
        bot.send_message(message.chat.id, "Upload complete!")
    else:
        bot.send_message(message.chat.id, "The downloaded file is empty. Please check the URL and try again.")


bot.polling()
