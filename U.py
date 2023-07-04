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
    bot.reply_to(message, "تم حفظ الرابط. كم رقم جلوس تريد؟")
    user_data[message.chat.id]['state'] = 'get_seat_count'

@bot.message_handler(func=lambda message: 'state' in user_data[message.chat.id] and user_data[message.chat.id]['state'] == 'get_seat_count')
def get_seat_count(message):
    seat_count = int(message.text)
    user_data[message.chat.id]['seat_count'] = seat_count
    user_data[message.chat.id]['seat_numbers'] = []
    bot.reply_to(message, "أدخل رقم الجلوس:")
    user_data[message.chat.id]['state'] = 'get_seats'

@bot.message_handler(func=lambda message: 'state' in user_data[message.chat.id] and user_data[message.chat.id]['state'] == 'get_seats')
def get_seats(message):
    seat_number = message.text
    user_data[message.chat.id]['seat_numbers'].append(seat_number)
    if len(user_data[message.chat.id]['seat_numbers']) < user_data[message.chat.id]['seat_count']:
        bot.reply_to(message, "أدخل رقم الجلوس:")
    else:
        bot.reply_to(message, "تم حفظ أرقام الجلوس. جاري الحصول على الدرجات...")
        get_grades(message.chat.id)

def get_grades(chat_id):
    url = user_data[chat_id]['url']
    seat_numbers = user_data[chat_id]['seat_numbers']
    for seat_number in seat_numbers:
        success = False
        error_count = 0
        while not success:
            try:
                # Send request to get page content
                response = requests.get(url)
                if response.status_code != 200:
                    error_count += 1
                    raise Exception(f"حدث خطأ {error_count}: الحالة {response.status_code}")
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find and fill seat number field
                seat_number_field = soup.find('input', {'id': 'ctl00_MainContent_TxtexamineeId'})
                if not seat_number_field:
                    error_count += 1
                    raise Exception(f"حدث خطأ {error_count}: لم يتم العثور على حقل رقم الجلوس")
                seat_number_field['value'] = seat_number
                # Find and click view grades button
                view_grades_button = soup.find('input', {'id': 'ctl00_MainContent_btnSearch'})
                if not view_grades_button:
                    error_count += 1
                    raise Exception(f"حدث خطأ {error_count}: لم يتم العثور على زر عرض الدرجات")
                view_grades_form = view_grades_button.find_parent('form')
                # Send request to submit form
                form_data = {}
                for field in view_grades_form.find_all('input'):
                    if field.get('name'):
                        form_data[field['name']] = field.get('value')
                response = requests.post(url, data=form_data)
                if response.status_code != 200:
                    error_count += 1
                    raise Exception(f"حدث خطأ {error_count}: الحالة {response.status_code}")
                # Send response to user
                soup = BeautifulSoup(response.text, 'html.parser')
                if "حدث خطأ" in soup.get_text():
                    error_count += 1
                    raise Exception(f"حدث خطأ {error_count}: لم يتم العثور على الدرجات")
                bot.send_message(chat_id, soup.get_text())
                success = True
            except Exception as e:
                bot.send_message(chat_id, str(e))

bot.polling()
