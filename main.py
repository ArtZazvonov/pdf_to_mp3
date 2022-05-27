import json
import telebot
import os
from dotenv import load_dotenv
import pdfplumber
from gtts import gTTS
from pathlib import Path
import markups as m
import requests as req
load_dotenv()
# config
token_tg = os.getenv('TG_TOKEN')

# bot init
bot = telebot.TeleBot(token_tg)

def file_write(file_path): # Открытие файла и соединение всех страниц
    with pdfplumber.PDF(open(file_path, mode='rb')) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    text = ''.join(pages)
    return text
def text_preparation(text): # Удаление из текста переносов строк
    text = text.replace('\n', '')
    return text
def convert_to_speech(text, file_path, language): # Преобразование текста в речь
    result_audio_file = gTTS(text, lang=language, slow=False)
    file_name = Path(file_path).stem
    result_audio_file.save(f'./files/audio/{file_name}.mp3')
def pdf_to_mp3(file_path='test.pdf', language='ru'): # Главная фенкция конвертации в речь
    if Path(file_path).is_file():
        print('Файл открыт...')
        text = file_write(file_path)
        print('Файл прочитан...')
        prepared_text = text_preparation(text)
        print('Подготовка текста заверщена...')
        convert_to_speech(prepared_text, file_path, language)
        print('Файл сохранён!')
        return
    else:
        return print('Не найден файл или он не в формате pdf')

def main():
    @bot.message_handler(commands=['start'])
    def start_function(message):
        bot.reply_to(message, f'Привет {message.from_user.first_name} я бот конвертер, могу преобразовать PDF книгу в аудио книгу.', reply_markup=m.source_markup)
    @bot.message_handler(commands=['help'])
    def help_function(message):
        bot.reply_to(message, f'Инструкции')
    @bot.message_handler(content_types=['text'])
    def help_function(message):
        if message.text.lower() == 'инструкции':
            bot.reply_to(message, f'Инструкции')
        if message.text.lower() == 'загрузить pdf':
            bot.reply_to(message, f'Отправь мне во вложении свою pdf книгу...')
    @bot.message_handler(func=lambda message: message.document.mime_type == 'application/pdf', content_types=['document'])
    def document_function(message):
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            text_src = './files/text/' + message.document.file_name
            with open(text_src, 'wb') as file:
                file.write(downloaded_file) # Сохранили файл в папку text
            pdf_to_mp3(text_src, "ru") # Вызываем главную функцию конвертирования
            audio_src = './files/audio/' + Path(text_src).stem + ".mp3"
            with open(audio_src, 'rb') as audio:
                bot.send_document(message.chat.id, audio)
        except Exception as e:
            bot.reply_to(message, e)
    @bot.message_handler(func=lambda message: message.document.mime_type != 'application/pdf', content_types=['document'])
    def document_function(message):
        bot.send_message(message.chat.id, f'Я думаю что это не pdf книга, проверь толи ты отправил.')




    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
