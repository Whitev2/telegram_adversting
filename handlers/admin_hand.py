import random

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.admin_kb import admin_menu, user_management, bot_management, bot_statistics
from keyboards.client_kb import main_menu
from orders_info.orders import Order
from states.admin_state import Admin

router = Router()

router.message.filter(state=Admin)  # После этой строки могут пройти только состояния из Executor
executor = Order(executor=True)
customer = Order(customer=True)


@router.message((F.text == "Управление пользователями"))
async def edit_balance(message: Message, state: FSMContext):
    await message.answer(f"Выберите интересующее вас действие:", reply_markup=user_management())


@router.message((F.text == "Управление ботом"))
async def edit_balance(message: Message, state: FSMContext):
    await message.answer(f"Выберите интересующее вас действие:", reply_markup=bot_management())


@router.message((F.text == "Статистика"))
async def edit_balance(message: Message, state: FSMContext):
    await message.answer(f"Выберите интересующее вас действие:", reply_markup=bot_statistics())


@router.message((F.text == "Назад в меню"))
async def edit_balance(message: Message, state: FSMContext):
    await message.answer(f"Добро пожаловать в админ панель", reply_markup=admin_menu())

@router.message((F.text == "Назад"))
async def edit_balance(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name
    await message.answer(f"{name},  здравствуйте!\n\nУ меня вы можете заказать рекламу или заработать, просматривая"
                         f" рекламу\n\nПодскажите, вы хотите заказать рекламу или заработать?",
                         reply_markup=await main_menu(message.from_user.id))


@router.message((F.text == "Редактировать баланс"))
async def edit_balance(message: Message, state: FSMContext):
    await state.set_state(Admin.edit_balance)
    await message.answer(f"Напишите user_id человека, кому хотитите изменить рекламный баланс", reply_markup=admin_menu())


@router.message(state=Admin.edit_balance)
async def edit_balance(message: Message, state: FSMContext):
    user_info = await customer.get_all_info(int(message.text))
    if user_info is not None:
        await state.update_data(user_id=int(message.text))
        await state.set_state(Admin.up_balance)
        await message.answer(f"Пользователь: @{user_info['username']}\n\n"
                             f"➖➖➖➖➖➖➖➖\n"
                             f"Рекламный баланс: {user_info['main_balance']}р.")
        await message.answer(f"Напишите сумму, которую хотите добавить к балансу", reply_markup=admin_menu())


@router.message(state=Admin.up_balance)
async def edit_balance(message: Message, state: FSMContext):
    try:
        if float(message.text) <= 5000:
            data = await state.get_data()
            user_id = data['user_id']
            await customer.top_up_balance(user_id, float(message.text))
            await state.set_state(Admin.edit_balance)
            await state.set_state(Admin.Admin_menu)
            await message.answer(f"Баланс был успешно пополнен", reply_markup=user_management())
        else:
            await message.answer("Простите, вы не можете изменить баланс более чем на 5000р за раз")
    except:
        await message.answer('Упс.. Кажется вы вводите не число')
