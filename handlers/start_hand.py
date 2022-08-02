import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data_base.db_use import about_the_executor, about_the_customer
from filters.admin_filters import IsAdmin
from keyboards.client_kb import main_menu, exercise_menu
from states.customer_states import Customer
from states.executor_states import Executor

router = Router()

@router.message(commands=['start', 'help'])
async def start(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name
    await message.answer(f"{name},  здравствуйте!\n\nУ меня вы можете заказать рекламу или заработать, просматривая"
                         f" рекламу\n\nПодскажите, вы хотите заказать рекламу или заработать?",
                         reply_markup=await main_menu(message.from_user.id))


@router.message((F.text == "Исполнитель"))
async def earn(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Executor.executor_menu)
    asyncio.create_task(start_add_base(message, collection='about_the_executor'))  # Запись в базу
    await message.answer(f"Какие задания вы хотите выполнять?", reply_markup=exercise_menu())


@router.message((F.text == "Заказчик"))
async def order(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Customer.customer_menu)
    asyncio.create_task(start_add_base(message, collection='about_the_customer'))  # Запись в базу
    await message.answer(f"Какие задания вы хотите создать?", reply_markup=exercise_menu())

@router.message((F.text == "Информация"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Информация")

@router.message((F.text == "Мой кабинет"))
async def my_cabinet(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Мой кабинет")

@router.message((F.text == "Админ панель"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Админка?")



async def start_add_base(message, collection: str):
    if collection == 'about_the_executor':
        await about_the_executor(message)
    elif collection == 'about_the_customer':
        await about_the_customer(message)
