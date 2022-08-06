from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

def info_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='Топ исполнителей', callback_data='top_exe')
    markup.button(text='Наш чат', url='https://t.me')
    markup.button(text='Задать вопрос', callback_data='question_from_user')
    markup.button(text='Правила', url='https://telegra.ph/Pravila-08-04-15')
    markup.button(text='Разработчики', callback_data='dev')
    markup.button(text='Закрыть', callback_data='close')
    markup.adjust(1, 1, 2, 1, 1)
    return markup.as_markup(resize_keyboard=True)
