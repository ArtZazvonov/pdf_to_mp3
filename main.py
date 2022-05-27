from dataclasses import replace
import pdfplumber
from gtts import gTTS
from pathlib import Path

def file_write(file_path):
    with pdfplumber.PDF(open(file_path, mode='rb')) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    text = ''.join(pages)
    return text
def text_preparation(text):
    text = text.replace('\n', '')
    return text

def pdf_to_mp3(file_path='test.pdf', language='ru'):
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        print('Файл открыт...')
        text = file_write(file_path)
        print('Файл прочитан...')
        prepared_text = text_preparation(text)
        print('Подготовка текста заверщена...')
        result_audio_file = gTTS(prepared_text, lang=language, slow=False)
        file_name = Path(file_path).stem
        result_audio_file.save(f'{file_name}.mp3')
        print('Файл сохранён!')
        return
    else:
        return print('Не найден файл или он не в формате pdf')

def main():
    pdf_to_mp3()
if __name__ == '__main__':
    main()
