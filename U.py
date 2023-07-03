import subprocess
import sys
import telebot
from bingpython import BingGPT

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('bingpython')

API_TOKEN = '6150964288:AAGJOF9HCaUBYmATYoNokDi4BHaKEQAS9UA'

bot = telebot.TeleBot(API_TOKEN)

gpt = BingGPT()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the AI Telegram Bot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = gpt.generate(message.text)
    bot.reply_to(message, response)

bot.polling()
