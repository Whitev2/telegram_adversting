import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data_base.db_use import about_the_executor, about_the_customer

router = Router()

@router.message(commands=['start', 'help'])
async def start(message: Message):
    name = message.from_user.first_name
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text="Заработать"))
    markup.row(types.KeyboardButton(text="Заказать рекламу"))
    await message.answer(f"{name},  здравствуйте!\n\nУ меня вы можете заказать рекламу или заработать, просматривая"
                         f" рекламу\n\nПодскажите, вы хотите заказать рекламу или заработать?",
                         reply_markup=markup.as_markup(resize_keyboard=True))


@router.message((F.text == "Заработать"))
async def earn(message: Message):
    asyncio.create_task(start_add_base(message, collection='about_the_executor'))  # Запись в базу
    markup = ReplyKeyboardBuilder()

    await message.answer(f"Меню для исполнителей")


@router.message((F.text == "Заказать рекламу"))
async def order(message: Message):
    asyncio.create_task(start_add_base(message, collection='about_the_customer'))  # Запись в базу
    markup = ReplyKeyboardBuilder()

    await message.answer(f"Меню для заказчиков")


async def start_add_base(message, collection: str):
    if collection == 'about_the_executor':
        await about_the_executor(message)
    elif collection == 'about_the_customer':
        await about_the_customer(message)
