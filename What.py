import os
import math
import telebot
from vidgear.gears import VideoGear

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)
chat_id = 'YOUR_CHAT_ID'

def send_video_info(filename):
    stream = VideoGear(source=filename).start()
    frame_count = 0
    while True:
        frame = stream.read()
        if frame is None:
            break
        frame_count += 1
    fps = stream.framerate
    stream.stop()
    duration = frame_count / fps
    size = os.path.getsize(filename) / (1024 * 1024)
    bot.send_message(chat_id, f'طول الفيديو: {duration} ثانية')
    bot.send_message(chat_id, f'مساحة الفيديو: {size:.2f} ميجابايت')

def trim_video(filename, start_time, end_time):
    options = {"-ss": start_time, "-t": end_time - start_time}
    stream = VideoGear(source=filename, logging=True, **options).start()
    trimmed_filename = f'trimmed_{start_time}_{end_time}_{filename}'
    writer = WriteGear(output_filename=trimmed_filename, logging=True)
    while True:
        frame = stream.read()
        if frame is None:
            break
        writer.write(frame)
    stream.stop()
    writer.close()
    return trimmed_filename

def split_video(filename, split_duration):
    stream = VideoGear(source=filename).start()
    frame_count = 0
    while True:
        frame = stream.read()
        if frame is None:
            break
        frame_count += 1
    fps = stream.framerate
    stream.stop()
    duration = frame_count / fps
    split_count = math.ceil(duration / split_duration)
    trimmed_filenames = []
    for i in range(split_count):
        start_time = i * split_duration
        end_time = min((i + 1) * split_duration, duration)
        trimmed_filename = trim_video(filename, start_time, end_time)
        trimmed_filenames.append(trimmed_filename)
    return trimmed_filenames

def send_and_delete_videos(videos):
    for video_filename in videos:
        video = open(video_filename, 'rb')
        bot.send_video(chat_id, video)
        os.remove(video_filename)

send_video_info('video.mp4')
split_duration = 30 * 60
trimmed_filenames = split_video('video.mp4', split_duration)

send_choice = input('هل تريد إرسال الفيديوهات المقصوصة وحذفها بعد الإرسال؟ (y/n) ')
if send_choice.lower() == 'y':
    send_and_delete_videos(trimmed_filenames)
