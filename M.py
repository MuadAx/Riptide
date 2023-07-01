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

try:
    import speedtest
except ImportError:
    install('speedtest-cli')
    import speedtest

TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def test_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000
    return download_speed, upload_speed

def split_text(text, max_length=4096):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "مرحبًا! أرسل لي رابط الموقع الذي تريد استخراج النص منه.")

@bot.message_handler(func=lambda message: True)
def get_text(message):
    url = message.text
    for i in range(3):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            continue
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    download_speed, upload_speed = test_speed()
    bot.send_message(message.chat.id, f'Download speed: {download_speed:.2f} Mbps\nUpload speed: {upload_speed:.2f} Mbps')
    for part in split_text(text):
        bot.send_message(message.chat.id, part)

bot.polling()
