import os
import math
import telebot
from moviepy.video.io.VideoFileClip import VideoFileClip

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)
chat_id = '1750552824'

def send_video_info(filename):
    clip = VideoFileClip(filename)
    duration = clip.duration
    size = os.path.getsize(filename) / (1024 * 1024)
    bot.send_message(chat_id, f'طول الفيديو: {duration} ثانية')
    bot.send_message(chat_id, f'مساحة الفيديو: {size:.2f} ميجابايت')

def trim_video(filename, start_time, end_time):
    clip = VideoFileClip(filename)
    trimmed_clip = clip.subclip(start_time, end_time)
    trimmed_filename = f'trimmed_{start_time}_{end_time}_{filename}'
    trimmed_clip.write_videofile(trimmed_filename)
    return trimmed_filename

def split_video(filename, split_duration):
    clip = VideoFileClip(filename)
    duration = clip.duration
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
