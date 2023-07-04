import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import telebot
except ImportError:
    install('pyTelegramBotAPI')
    import telebot

try:
    from bs4 import BeautifulSoup
except ImportError:
    install('beautifulsoup4')
    from bs4 import BeautifulSoup

try:
    import requests
except ImportError:
    install('requests')
    import requests

from concurrent.futures import ThreadPoolExecutor
import random

TOKEN = '5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw'
bot = telebot.TeleBot(TOKEN)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

request_count = 0
count_message = None

def fetch(url):
    global request_count, count_message
    for i in range(3):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            request_count += 1
            if count_message:
                bot.edit_message_text(f"عدد الطلبات: {request_count}", count_message.chat.id, count_message.message_id)
            if request_count >= 40:
                bot.send_message(count_message.chat.id, "معاذ الموقع عليه ضغط")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            continue

@bot.message_handler(commands=['start'])
def start(message):
    global count_message
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي رابط الموقع الذي تريد استخراج النص منه.")
    count_message = bot.send_message(message.chat.id, f"عدد الطلبات: {request_count}")

@bot.message_handler(func=lambda message: True)
def get_text(message):
    url = message.text
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch, url)
        response_text = future.result()
    response_text.encoding = 'utf-8'
    soup = BeautifulSoup(response_text, 'html.parser')
    text = soup.get_text()
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, "Muad Ax everything done")
    
    inputs = soup.find_all('input')
    for input_element in inputs:
        if input_element.get('type') == 'text':
            random_number = ''.join([str(random.randint(0,9)) for _ in range(5)])
            input_element['value'] = random_number
    
    new_url = soup.find('form').get('action')
    bot.send_message(message.chat.id, new_url)

bot.polling()
