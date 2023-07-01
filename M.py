import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import telebot
except ImportError:
    install('telebot')
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

TOKEN = '6150964288:AAGJOF9HCaUBYmATYoNokDi4BHaKEQAS9UA'
bot = telebot.TeleBot(TOKEN)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

with open('pr.txt', 'r') as f:
    proxies_list = [line.strip() for line in f]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي رابط الموقع الذي تريد استخراج النص منه.")

@bot.message_handler(func=lambda message: True)
def get_text(message):
    url = message.text
    proxy = random.choice(proxies_list)
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            continue
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    bot.send_message(message.chat.id, text)

bot.polling()
