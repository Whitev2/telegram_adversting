import random

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from orders_info.orders import Order
from keyboards.client_inline import telegram
from keyboards.client_kb import main_menu
from states.executor_states import Executor

router = Router()

router.message.filter(state=Executor)  # После этой строки могут пройти только состояния из Executor
order = Order(executor=True)


@router.message((F.text == "Телеграм"))
async def info(message: Message):
    await message.answer(f"Все телеграм задания для выполниния", reply_markup=await telegram(message, 'executor'))


@router.message((F.text == "Другие задания"))
async def info(message: Message):
    await message.answer(f"Все другие задания для выполниния")


@router.message((F.text == "Назад в меню"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Хорошо, возврат в меню..", reply_markup=await main_menu(message))


@router.callback_query(lambda call: 'executor' in call.data and 'channel' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    orders_for_user = await order.order_to_be_executed(query.from_user.id,
                                                       'channel')  # получает рандомную непросмотренную новость
    if orders_for_user is not None:
        markup = InlineKeyboardBuilder()
        markup.button(text='Выполнить', url=orders_for_user['link'])
        markup.button(text='Проверить', callback_data=f'check_execution {orders_for_user["_id"]}')
        markup.button(text='Пропустить', callback_data=f'next_channel')
        markup.button(text='Назад в меню', callback_data=f'back_to_executor_menu')
        markup.adjust(1, 1, 1, 1)
        await query.message.answer('Задание: "Подписаться на канал"\n\n'
                                   f'Стоимость: {orders_for_user["click_price"]}\n\n'
                                   'После выполнения, нажмите "Проверить"', reply_markup=markup.as_markup())
    else:
        await query.message.answer('На сегодня задания с каналами закончились, но вы можете перейти к другим заданиям!')


@router.callback_query(lambda call: 'check_execution' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    data = query.data.split()
    order_id = data[-1]
    # проверить что человек подписался,
    # если подписался то отправить некст новстьб если нет то вывести уведомление об ошибке
    await query.message.delete()
    await order.add_complete_order(query.from_user.id, order_id)
    orders_for_user = await order.order_to_be_executed(query.from_user.id,
                                                       'channel')  # получает рандомную непросмотренную новость
    if orders_for_user is not None:
        markup = InlineKeyboardBuilder()
        markup.button(text='Выполнить', url=orders_for_user['link'])
        markup.button(text='Проверить', callback_data=f'check_execution {orders_for_user["_id"]}')
        markup.button(text='Пропустить', callback_data=f'next_channel')
        markup.button(text='Назад в меню', callback_data=f'back_to_executor_menu')
        markup.adjust(1, 1, 1, 1)
        await query.message.answer('Задание: "Подписаться на канал"\n\n'
                                   f'Стоимость: {orders_for_user["click_price"]}\n\n'
                                   'После выполнения, нажмите "Проверить"', reply_markup=markup.as_markup())
    else:
        await query.message.answer('На сегодня задания с каналами закончились, но вы можете перейти к другим заданиям!')


@router.callback_query(lambda call: 'next_channel' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    orders_for_user = await order.order_to_be_executed(query.from_user.id,
                                                       'channel')  # получает рандомную непросмотренную новость
    if orders_for_user is not None:
        markup = InlineKeyboardBuilder()
        markup.button(text='Выполнить', url=orders_for_user['link'])
        markup.button(text='Проверить', callback_data=f'check_execution {orders_for_user["_id"]}')
        markup.button(text='Пропустить', callback_data=f'next_channel')
        markup.button(text='Назад в меню', callback_data=f'back_to_executor_menu')
        markup.adjust(1, 1, 1, 1)
        await query.message.answer('Задание: "Подписаться на канал"\n\n'
                                   f'Стоимость: {orders_for_user["click_price"]}\n\n'
                                   'После выполнения, нажмите "Проверить"', reply_markup=markup.as_markup())
    else:
        await query.message.answer('На сегодня задания с каналами закончились, но вы можете перейти к другим заданиям!')


@router.callback_query(lambda call: 'executor' in call.data and 'post' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(str(query.data.split()))
