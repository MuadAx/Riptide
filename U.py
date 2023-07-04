import subprocess
import sys
import time

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
success_count = 0
fail_count = 0
start_time = time.time()
count_message = None

session = requests.Session()

def fetch(url):
    global request_count, success_count, fail_count, start_time, count_message
    for i in range(3):
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
            request_count += 1
            success_count += 1
            if count_message:
                bot.edit_message_text(f"عدد الطلبات: {request_count}\nعدد الطلبات الناجحة: {success_count}\nعدد الطلبات الفاشلة: {fail_count}", count_message.chat.id, count_message.message_id)
            if time.time() - start_time >= 300 and request_count == 0:
                bot.send_message(count_message.chat.id, "معاذ الموقع عليه ضغط")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            fail_count += 1
            continue

@bot.message_handler(commands=['start'])
def start(message):
    global count_message
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي رابط الموقع الذي تريد استخراج النص منه.")
    count_message = bot.send_message(message.chat.id, f"عدد الطلبات: {request_count}\nعدد الطلبات الناجحة: {success_count}\nعدد الطلبات الفاشلة: {fail_count}")

@bot.message_handler(func=lambda message: True)
def get_text(message):
    url = message.text
    
    msg = bot.send_message(message.chat.id, "ما هو رقم جلوسك؟")
    bot.register_next_step_handler(msg, process_seat_number_step, url)

def process_seat_number_step(message, url):
    seat_number = message.text
    
    with ThreadPoolExecutor() as executor:
        future = executor.submit(fetch, url)
        response_text = future.result()
    
    response_text.encoding = 'utf-8'
    soup = BeautifulSoup(response_text, 'html.parser')
    
    inputs = soup.find_all('input')
    
    for input_element in inputs:
        if input_element.get('name') == 'seat_number':
            input_element['value'] = seat_number
    
bot.polling()
