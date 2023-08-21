# import the libraries
import fitz
import telebot

# create a bot object using your token
bot = telebot.TeleBot ("5566197914:AAHIoqN-wclAi8BU6vAnR_b5HQP07yPNKMw")

# define a handler function that will be called when the bot receives a document message
@bot.message_handler (content_types=['document'])
def handle_document (message):
    # download the document
    file_info = bot.get_file (message.document.file_id)
    downloaded_file = bot.download_file (file_info.file_path)
    # convert it to text
    pdf_file = fitz.open (stream=downloaded_file, filetype='pdf')
    text = ""
    for page in pdf_file:
        text += page.getText ()
    # send the text back
    bot.send_message (message.chat.id, text)

# start polling for updates
bot.polling ()
