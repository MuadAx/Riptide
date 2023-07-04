import requests
from bs4 import BeautifulSoup
import telebot

bot_token = "6150964288:AAGJOF9HCaUBYmATYoNokDi4BHaKEQAS9UA"
bot = telebot.TeleBot(bot_token)

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أدخل رابط الموقع الخاص بك:")
    user_data[message.chat.id] = {}

@bot.message_handler(func=lambda message: 'url' not in user_data[message.chat.id])
def get_url(message):
    url = message.text
    user_data[message.chat.id]['url'] = url
    bot.reply_to(message, "تم حفظ الرابط. أدخل رقم الجلوس الخاص بك:")

@bot.message_handler(func=lambda message: 'seat_number' not in user_data[message.chat.id])
def get_seat_number(message):
    seat_number = message.text
    user_data[message.chat.id]['seat_number'] = seat_number
    bot.reply_to(message, "تم حفظ رقم الجلوس. جاري الحصول على الدرجات...")
    get_grades(message.chat.id)

def get_grades(chat_id):
    url = user_data[chat_id]['url']
    seat_number = user_data[chat_id]['seat_number']
    while True:
        # Send request to get page content
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find and fill seat number field
        seat_number_field = soup.find('input', {'id': 'ctl00_MainContent_TxtexamineeId'})
        seat_number_field['value'] = seat_number
        # Find and click view grades button
        view_grades_button = soup.find('input', {'id': 'ctl00_MainContent_btnSearch'})
        view_grades_form = view_grades_button.find_parent('form')
        # Send request to submit form
        form_data = {}
        for field in view_grades_form.find_all('input'):
            if field.get('name'):
                form_data[field['name']] = field.get('value')
        response = requests.post(url, data=form_data)
        # Send response to user
        soup = BeautifulSoup(response.text, 'html.parser')
        bot.send_message(chat_id, soup.get_text())
print("hi")
bot.polling()
