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

from concurrent.futures import ThreadPoolExecutor, as_completed
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

def fetch(url, seat_number):
    global request_count, success_count, fail_count, start_time, count_message
    for i in range(3):
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
            request_count += 1
            
            response_text = response.text
            response_text.encoding = 'utf-8'
            soup = BeautifulSoup(response_text, 'html.parser')
            
            inputs = soup.find_all('input')
            
            for input_element in inputs:
                if input_element.get('name') == 'رقم الجلوس':
                    input_element['value'] = seat_number
            
            view_grades_button = soup.find('input', {'value': 'عرض الدرجات'})
            if view_grades_button:
                view_grades_form = view_grades_button.find_parent('form')
                if view_grades_form:
                    action_url = view_grades_form.get('action')
                    method = view_grades_form.get('method', 'get').lower()
                    data = {}
                    for input_element in view_grades_form.find_all('input'):
                        name = input_element.get('name')
                        value = input_element.get('value')
                        if name and value:
                            data[name] = value
                    
                    if method == 'post':
                        response = session.post(action_url, data=data, headers=headers)
                    else:
                        response = session.get(action_url, params=data, headers=headers)
                    
                    response.raise_for_status()
                    
                    response_text = response.text
                    response_text.encoding = 'utf-8'
                    soup = BeautifulSoup(response_text, 'html.parser')
            
            success_count += 1
            
            if count_message:
                elapsed_time = time.time() - start_time
                requests_per_second = request_count / elapsed_time if elapsed_time > 0 else 0
                bot.edit_message_text(f"عدد الطلبات: {request_count}\nعدد الطلبات الناجحة: {success_count}\nعدد الطلبات الفاشلة: {fail_count}\nالطلبات في الثانية: {requests_per_second:.2f}", count_message.chat.id, count_message.message_id)
            if time.time() - start_time >= 300 and request_count == 0:
                bot.send_message(count_message.chat.id, "معاذ الموقع عليه ضغط")
            
            return str(soup)
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
    
    while True:
        response_text = fetch(url, seat_number)
        bot.send_message(message.chat.id, response_text)
        time.sleep(60)
    
bot.polling()
