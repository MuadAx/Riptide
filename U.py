import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('transformers')
install('bingpython')
install('EdgeGpt')
install('GoogleBard')
import telebot
from transformers import pipeline
from EdgeGpt import EdgeGpt
from bingpython import BingGPT

API_TOKEN = '6150964288:AAGJOF9HCaUBYmATYoNokDi4BHaKEQAS9UA'

bot = telebot.TeleBot(API_TOKEN)

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
gpt1 = EdgeGpt()
gpt2 = BingGPT()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the AI Telegram Bot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response1 = generator(message.text, max_length=50)[0]['generated_text']
    response2 = gpt1.generate(message.text)
    response3 = gpt2.generate(message.text)
    bot.reply_to(message, f"GPT-Neo: {response1}\nEdgeGpt: {response2}\nBingGPT: {response3}")
print("hi")
bot.polling()
