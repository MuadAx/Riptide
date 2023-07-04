from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
    driver = webdriver.Firefox()
    driver.get(url)
    # Enter seat number
    seat_number_field = driver.find_element_by_id("txtSeatNo")
    seat_number_field.send_keys(seat_number)
    # Click on view grades button
    view_grades_button = driver.find_element_by_id("btnShow")
    view_grades_button.click()
    # Take screenshot
    driver.save_screenshot("grades.png")
    # Send screenshot to user
    photo = open('grades.png', 'rb')
    bot.send_photo(chat_id, photo)
    driver.quit()

bot.polling()
