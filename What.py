import telebot
import os

bot = telebot.TeleBot('5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw')

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    file_name, file_ext = os.path.splitext(file_info.file_path)
    with open(f'video{file_ext}', 'wb') as new_file:
        new_file.write(downloaded_file)

    size = os.path.getsize(f'video{file_ext}')
    size = round(size / (1024 * 1024), 2)
    bot.reply_to(message, f'صيغة الفيديو: {file_ext[1:]}\nمساحة الفيديو: {size} ميجابايت')

    video = open('video.mp4', 'rb')
    bot.send_video(message.chat.id, video)

bot.polling()
