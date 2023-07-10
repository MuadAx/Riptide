import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)

def download_fb_video(video_url, file_name):
    html = requests.get(video_url)
    soup = BeautifulSoup(html.text, 'html.parser')
    video_links = soup.find_all('a', href=True)
    for link in video_links:
        if 'hd_src' in link['href']:
            video_link = link['href'].split('hd_src:"')[1].split('",sd_src:"')[0]
            break
        elif 'sd_src' in link['href']:
            video_link = link['href'].split('sd_src:"')[1].split('",hd_tag:"')[0]
            break
    video_data = requests.get(video_link).content
    with open(file_name, 'wb') as f:
        f.write(video_data)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي رابط الفيديو الذي ترغب في تنزيله.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_url = message.text
    file_name = 'video.mp4'
    download_fb_video(video_url, file_name)
    video = open(file_name, 'rb')
    bot.send_video(message.chat.id, video)

bot.polling()
