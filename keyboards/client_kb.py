from aiogram import types
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data import Data

data = Data()

async def main_menu(t_id):
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Исполнитель'))
    markup.row(types.KeyboardButton(text='Заказчик'))
    markup.row(types.KeyboardButton(text='Информация'))
    markup.row(types.KeyboardButton(text='Мой кабинет'))
    if t_id in data.admins:
        markup.row(types.KeyboardButton(text='Админ панель'))
    markup.adjust(2, 1, 1)
    return markup.as_markup(resize_keyboard=True)


def exercise_menu():
    print(1)
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Телеграм'))
    markup.row(types.KeyboardButton(text='Другие задания'))
    markup.row(types.KeyboardButton(text='Назад в меню'))
    return markup.as_markup(resize_keyboard=True)