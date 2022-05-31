import telebot
import os
from dotenv import load_dotenv
import pdfplumber
from gtts import gTTS # Google
import pyttsx3 # Встроенные
from pathlib import Path
import markups as m
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
def convert_to_speech_gTTS(text, file_path, language): # Преобразование текста в речь google
    tts = gTTS(text, lang=language, slow=False)
    tts.save(f'./files/audio/{Path(file_path).stem}.mp3')
def convert_to_speech_pyTTSx3(text, file_path): # Преобразование текста в речь microsoft
    tts = pyttsx3.init()
    tts.setProperty('rate', 140)
    tts.say(text)
    tts.save_to_file(text , f'./files/audio/{Path(file_path).stem}.mp3')
    tts.runAndWait()
    tts.stop()
def pdf_to_mp3(file_path, language='ru'): # Главная фенкция конвертации в речь
    if Path(file_path).is_file():
        print('Файл открыт...')
        text = file_write(file_path)
        print('Файл прочитан...')
        prepared_text = text_preparation(text)
        print('Подготовка текста заверщена...')
        convert_to_speech_gTTS(prepared_text, file_path, language) # Преобразование текста в речь google
        # convert_to_speech_pyTTSx3(prepared_text, file_path) # Преобразование текста в речь microsoft
        print('Файл сохранён!')
        return
    else:
        return print('Не найден файл или он не в формате pdf')
def clear_folder(file_path, file_name):
    os.remove(file_path + file_name)
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
    @bot.message_handler(content_types=['document'])
    def document_function(message):
        if message.document.mime_type == 'application/pdf':
            try:
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                text_src = './files/text/' + message.document.file_name
                with open(text_src, 'wb') as file:
                    file.write(downloaded_file) # Сохранили файл в папку
                pdf_to_mp3(text_src, "ru") # Вызываем главную функцию конвертирования
                audio_src = './files/audio/' + Path(text_src).stem + ".mp3"
                with open(audio_src, 'rb') as audio:
                    bot.send_document(message.chat.id, audio)
                clear_folder('./files/audio/', Path(text_src).stem + ".mp3")
                clear_folder('./files/text/', message.document.file_name)
            except Exception as e:
                bot.reply_to(message, e)
        else:
            bot.send_message(message.chat.id, f'Я думаю что это не pdf книга, проверь толи ты отправил.')

    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
