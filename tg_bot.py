BOT_TOKEN = "7901737372:AAF8qhNGjuogfJBWsixq_eM6Ookn_JiVVlg"
import os
import telebot
from PIL import Image
import pytesseract

bot = telebot.TeleBot(BOT_TOKEN)
pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def add(message):
    a = int(message.text.split()[0])
    b = int(message.text.split()[1])
    bot.reply(message, a + b)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    id = message.photo[-1].file_id
    info = bot.get_file(id)
    path = info.file_path
    downloaded_file = bot.download_file(path)
    image_path = "image.jpg"
    with open(image_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="eng")
    if text:
        bot.send_photo(message.chat.id, photo=open(image_path, 'rb'), caption=text)
    else:
        bot.reply_to(message, "Text not found")
    os.remove(image_path)

bot.infinity_polling()