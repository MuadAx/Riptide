import os
from telebot import TeleBot

bot = TeleBot('5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw')
chat_id = '1750552824'
file_path = 'video.mp4'
max_size = 50 * 1024 * 1024 # 50 MB

file_size = os.path.getsize(file_path)
if file_size > max_size:
    # split the file into two parts
    with open(file_path, 'rb') as f:
        data = f.read()
        part1 = data[:file_size//2]
        part2 = data[file_size//2:]
    
    # save the parts to separate files
    with open('part1.mp4', 'wb') as f:
        f.write(part1)
    with open('part2.mp4', 'wb') as f:
        f.write(part2)
    
    # send the parts using telebot
    with open('part1.mp4', 'rb') as f:
        bot.send_video(chat_id, f)
    with open('part2.mp4', 'rb') as f:
        bot.send_video(chat_id, f)
else:
    # send the file as is
    with open(file_path, 'rb') as f:
        bot.send_video(chat_id, f)
