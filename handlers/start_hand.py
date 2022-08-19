import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from filters.admin_filters import IsAdmin
from keyboards.admin_kb import admin_menu
from keyboards.client_kb import main_menu, exercise_menu
from keyboards.infobot_inline import info_menu
from orders_info.user_info import Users
from states.admin_state import Admin
from states.customer_states import Customer
from states.executor_states import Executor

router = Router()
user = Users()


@router.message(commands=['start', 'help'])
async def start(message: Message, state: FSMContext):
    await state.clear()
    data = await state.get_data()
    print(data)
    await user.new_user(message)
    name = message.from_user.first_name
    await message.answer(f"{name},  здравствуйте!\n\nУ меня вы можете заказать рекламу или заработать, просматривая"
                         f" рекламу\n\nПодскажите, вы хотите заказать рекламу или заработать?",
                         reply_markup=await main_menu(message.from_user.id))


@router.message((F.text == "Исполнитель"))
async def earn(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Executor.executor_menu)
    await message.answer(f"Какие задания вы хотите выполнять?", reply_markup=exercise_menu())


@router.message((F.text == "Заказчик"))
async def order(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Customer.customer_menu)
    await message.answer(f"Какие задания вы хотите создать?", reply_markup=exercise_menu())


@router.message((F.text == "Информация"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Тут вы можете:\n\n"
                            f"— Ознакомиться со списком лучших исполнителей\n"
                            f"— Найти ответ на интересующий вас вопрос\n"
                            f"— Предложить новую идею или сообщить о баге", reply_markup=info_menu())


@router.message((F.text == "Админ панель"))
async def admin_panel(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Admin.Admin_menu)
    await message.answer(f"Добро пожаловать в админ панель", reply_markup=admin_menu())

