import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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

async def earn_base(message):
    pass

@router.message((F.text == "Заказать рекламу"))
async def order(message: Message):
    asyncio.create_task(start_add_base(message, collection='about_the_customer'))  # Запись в базу
    markup = ReplyKeyboardBuilder()

    await message.answer(f"Меню для заказчиков")


async def start_add_base(message, collection: str):
    if collection:
        pass
    user_id = message.from_user.id
    username = message.from_user.username
    user_firstname = message.from_user.first_name
    user_language = message.from_user.language_code
    print(f"{user_id}\n{username}\n{user_firstname}\n{user_language}")