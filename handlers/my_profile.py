import random
from datetime import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.admin_kb import admin_menu, user_management, bot_management, bot_statistics
from keyboards.client_inline import profile_menu
from keyboards.client_kb import main_menu
from orders_info.orders import Order
from orders_info.user_info import Users
from payments.lava import Lava

from states.admin_state import Admin
from states.pay_states import Pay

router = Router()

user = Users()
lava = Lava()

@router.message((F.text == "Мой кабинет"))
async def edit_balance(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_info = await user.get_all_info(telegram_id=user_id)
    date =  datetime.now() - user_info['datetime_come']
    await message.answer(f"Ваш ID: {user_id}\n"
                         f"Дней в боте: {date.days}\n"
                         f"Статус: {user_info['level']}\n"
                         f"Имя: {message.from_user.first_name}\n"
                         f"Юзернейм: @{message.from_user.username}\n"
                         f"Ваш наставник: [[Реферер]]\n\n"
                         f"--------------------\n\n"
                         f"Подписок на канал: [[из базы]]\n"
                         f"Просмотров постов: [[из базы]]\n"
                         f"Вступлений в группы: [[из базы]]\n"
                         f"Выполнено заданий: [[из базы]]\n"
                         f"Переходов по ссылкам: [[из базы]]\n"
                         f"Получено бонусов: [[из базы]]р.\n\n"
                         f"--------------------\n\n"
                         f"Основной баланс: {user_info['main_balance']}р.\n"
                         f"Рекламный баланс: {user_info['advertising_balance']}р.\n"
                         f"Заработано всего: {user_info['all_time_main_balance']}р.\n"
                         f"Заработано с рефералов: [[из базы]]р.\n"
                         f"Штрафов с рефералов: [[из базы]]р.\n"
                         f"Штрафы: {user_info['main_fines']}р.\n\n"
                         f"--------------------\n\n"
                         f"Пополнено всего: {user_info['all_time_deposit_advs']}р.\n"
                         f"Выведено всего: {user_info['all_time_withdrawal']}р.\n"
                         f"Ожидается к выплате: [[из базы]]р.\n"
                         f"Потрачено на рекламу: [[из базы]]р.", reply_markup=profile_menu())


@router.callback_query(lambda call: call.data == 'deposit/withdraw')
async def deposit_withdraw(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    markup = InlineKeyboardBuilder()
    markup.button(text='Пополнить рекламный', callback_data=f'deposit')
    markup.button(text='Вывести основной', callback_data=f'withdraw')
    markup.adjust(1, 1, 2)
    await query.message.answer('Выберите интересующее вас действие', reply_markup=markup.as_markup())


@router.callback_query(lambda call: call.data == 'deposit' or 'replenish_the_balance' in call.data)
async def deposit_withdraw(query: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardBuilder()
    markup.button(text='Lawa', callback_data=f'Lawa')
    if 'replenish_the_balance' in query.data:
        pass
    await query.message.delete()
    await query.message.answer("Выберите способ оплаты:", reply_markup=markup.as_markup())


@router.callback_query(lambda call: call.data == 'Lawa')
async def deposit(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Pay.deposit_sum)
    await query.message.answer('Напишите сумму пополнения')

@router.message(state=Pay.deposit_sum)
async def deposit_sum(message: Message, state: FSMContext):
    order = '1'
    deposit_url = await lava.create_deposit(deposit_sum=message.text, deposit_id=order)
    markup = InlineKeyboardBuilder()
    markup.button(text='Оплатить', web_app=WebAppInfo(url=deposit_url))
    markup.button(text='Я оплатил', callback_data=f'check_deposit {order}')
    markup.adjust(1)
    await message.answer(f'Пополнение баланса на {message.text}р', reply_markup=markup.as_markup())

@router.callback_query(lambda call: 'check_deposit' in call.data)
async def deposit(query: types.CallbackQuery, state: FSMContext):
    order = query.data.split()[-1]
    deposit_info = await lava.check_deposit_status(order)
    try:
        if deposit_info['status'] == 'success':
            await query.message.answer("Оплата прошла успешно")
    except:
        await query.answer("Ошибка! Оплата не поступила")


@router.callback_query(lambda call: call.data == 'buy_premium')
async def deposit_withdraw(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("Примиум доступ с дополнительными возможностями")

@router.callback_query(lambda call: call.data == 'history')
async def deposit_withdraw(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer("История оплат/выводов и чеки")