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

executor = Order(executor=True)
customer = Order(customer=True)


@router.message((F.text == "Мой кабинет"))
async def edit_balance(message: Message, state: FSMContext):
    executor_info = await executor.get_all_info(message.from_user.id)
    customer_info = await customer.get_all_info(message.from_user.id)
    await message.answer(f"Ваш ID: {message.from_user.id}\n"
                         f"Дней в боте: [[Из базы]]\n"
                         f"Статус: {executor_info['level']}\n"
                         f"Имя: {message.from_user.first_name}\n"
                         f"Юзернейм: @{message.from_user.username}\n"
                         f"Ваш наставник: [[Реферер]]\n\n"
                         f"--------------------\n\n"
                         f"Подписок на канал: [[из базы]]\n"
                         f"Просмотров постов: [[из базы]]\n"
                         f"Вступлений в группы: [[из базы]]\n"
                         f"Выполнено заданий: [[из базы]]\n"
                         f"Переходов по ссылкам: [[из базы]]\n"
                         f"Получено бонусов: [[из базы]]\n\n"
                         f"--------------------\n\n"
                         f"Заработано всего: [[из базы]]\n"
                         f"Заработано с рефералов: [[из базы]]\n"
                         f"Штрафов с рефералов: [[из базы]]\n"
                         f"Штрафы: [[из базы]]\n\n"
                         f"--------------------\n\n"
                         f"Пополнено всего: [[из базы]]\n"
                         f"Выведено всего: [[из базы]]\n"
                         f"Ожидается к выплате: [[из базы]]\n"
                         f"Потрачено на рекламу: [[из базы]]")
