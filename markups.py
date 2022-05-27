from telebot import types
source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
source_markup_btn1 = types.KeyboardButton('инструкции')
source_markup_btn2 = types.KeyboardButton('загрузить pdf')
source_markup.add(source_markup_btn1, source_markup_btn2)
