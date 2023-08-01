import os
import sys
from io import BytesIO

def install(package):
    os.system(f"{sys.executable} -m pip install {package}")

try:
    from telebot import TeleBot
except ImportError:
    install('pyTelegramBotAPI')
    from telebot import TeleBot

try:
    from PIL import Image
except ImportError:
    install('Pillow')
    from PIL import Image

TOKEN = '5489808608:AAEOhM0raBXapeGbGwxtlZTPwN0fYuxBmEI'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أرسل لي الصور التي تريد تحويلها إلى ملف PDF. عندما تنتهي، أرسل /pdf لإنشاء الملف.")

images = []

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)
    image = Image.open(BytesIO(file))
    images.append(image)

@bot.message_handler(commands=['pdf'])
def create_pdf(message):
    if not images:
        bot.reply_to(message, "لم ترسل أي صور بعد.")
        return

    output = BytesIO()
    images[0].save(output, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    output.seek(0)
    bot.send_document(message.chat.id, output, caption="هذا هو ملف PDF الخاص بك.")
    images.clear()

bot.polling()
