from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_menu():
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Управление пользователями'))
    markup.row(types.KeyboardButton(text='Управление ботом'))
    markup.row(types.KeyboardButton(text='Статистика'))
    markup.row(types.KeyboardButton(text='Назад'))
    return markup.as_markup(resize_keyboard=True)

def user_management():
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Редактировать баланс'))
    markup.row(types.KeyboardButton(text='Статистика пользователя'))
    markup.row(types.KeyboardButton(text='Информация о пользователе'))
    markup.row(types.KeyboardButton(text='Назад в меню'))
    return markup.as_markup(resize_keyboard=True)

def bot_management():
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Посмотреть логи'))
    markup.row(types.KeyboardButton(text='Рассылка'))
    markup.row(types.KeyboardButton(text='Технический режим'))
    markup.row(types.KeyboardButton(text='Назад в меню'))
    return markup.as_markup(resize_keyboard=True)


def bot_statistics():
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Статистика за сутки'))
    markup.row(types.KeyboardButton(text='Статистика за всё время'))
    markup.row(types.KeyboardButton(text='Назад в меню'))
    return markup.as_markup(resize_keyboard=True)

