import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('EdgeGpt')
install('bingpython')

import telebot
from EdgeGpt import EdgeGpt
from bingpython import BingGPT

API_TOKEN = '<your_token_here>'

bot = telebot.TeleBot(API_TOKEN)

gpt1 = EdgeGpt()
gpt2 = BingGPT()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the AI Telegram Bot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response1 = gpt1.generate(message.text)
    response2 = gpt2.generate(message.text)
    bot.reply_to(message, f"EdgeGpt: {response1}\nBingGPT: {response2}")

bot.polling()
