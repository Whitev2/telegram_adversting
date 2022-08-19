import random
import re

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import Data
from orders_info.orders import Order
from keyboards.client_inline import telegram
from keyboards.client_kb import main_menu, exercise_menu
from states.executor_states import Executor
from tools.chats_check import member_status

router = Router()
data = Data()
bot = data.get_bot()

router.message.filter(state=Executor)  # После этой строки могут пройти только состояния из Executor
order = Order()


@router.message((F.text == "Телеграм"))
async def info(message: Message):
    await message.answer(f"В этом разделе вы должны выполнять задания в Telegram.\n\n"
                         f"После автоматической проверки, вам будет начислена сумма в соответствии с заданием.\n\n"
                         f"Выберите интересующие вас задания:"
                         , reply_markup=await telegram(message, 'executor'))


@router.message((F.text == "Другие задания"))
async def info(message: Message):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='！Приступить к выполнению',
                                          callback_data=f'executor {message.from_user.id} other_task'))
    await message.answer(f"В этом разделе вы должны выполнять задания и отправлять его на проверку заказчику.\n\n"
                         f"После проверки выполненной вами работы заказчиком,"
                         f" вам будет начислена сумма в соответствии с заданием.\n"
                         f"Также заказчик может отправить ваше выполнение на доработку."
                         f" Если возникают споры - обращайтесь в поддержку.",
                         reply_markup=markup.as_markup(resize_keyboard=True))


@router.message((F.text == "Назад в меню"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Главное меню:", reply_markup=await main_menu(message.from_user.id))


"****************************************************** CHANNEL *******************************************************"


@router.callback_query(lambda call: 'executor' in call.data and 'channel' in call.data or 'channel_next' in call.data)
async def channel(query: types.CallbackQuery, state: FSMContext):
    new_order = await order.order_to_be_executed(query.from_user.id, 'channel')
    order_link = new_order['link']
    chat_id = new_order['chat_id']
    await state.update_data(order_link=order_link)
    await state.update_data(chat_id=chat_id)
    if new_order is not None:
        await query.message.delete()
        markup = InlineKeyboardBuilder()
        markup.row(types.InlineKeyboardButton(text='Выполнить', url=order_link))
        markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='channel_verify'))
        markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='channel_next'))
        markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
        markup.adjust(1, 1, 1, 1)
        await query.message.answer("Задание: 'Подписаться на канал'\n\n"
                                   f"Стоимость: {new_order['click_price']}", reply_markup=markup.as_markup())
    else:
        await query.message.answer("Задания закончились")


@router.callback_query(lambda call: 'channel_verify' in call.data)
async def channel_verify(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = data['chat_id']
    order_link = data['order_link']
    print(chat_id)
    print(order_link)
    user_status = await member_status(chat_id, query.from_user.id)
    if user_status:
        new_order = await order.order_to_be_executed(query.from_user.id, 'channel')
        order_link = new_order['link']
        chat_id = new_order['chat_id']
        await state.update_data(order_link=order_link)
        await state.update_data(chat_id=chat_id)
        if new_order is not None:
            await query.message.delete()
            markup = InlineKeyboardBuilder()
            markup.row(types.InlineKeyboardButton(text='Выполнить', callback_data=order_link))
            markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='channel_verify'))
            markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='channel_next'))
            markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
            await query.message.answer("Задание: 'Подписаться на канал'\n\n"
                                       f"Стоимость: {new_order['click_price']}", reply_markup=markup.as_markup())
        else:
            await query.message.answer("Задания закончились")
    else:
        await query.answer("Ошибка! Вы не подписались на канал")


"******************************************************* GROUP ********************************************************"


@router.callback_query(lambda call: 'executor' in call.data and 'group' in call.data or 'group_next' in call.data)
async def group(query: types.CallbackQuery, state: FSMContext):
    new_order = await order.order_to_be_executed(query.from_user.id, 'group')
    if new_order is not None:
        markup = InlineKeyboardBuilder()
        markup.row(types.InlineKeyboardButton(text='Выполнить', callback_data=new_order['link']))
        markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='group_verify'))
        markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='group_next'))
        markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
    else:
        await query.message.answer("Задания закончились")


@router.callback_query(lambda call: 'executor' in call.data and 'group_verify' in call.data)
async def group_verify(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chat_id = data['chat_id']
    user_status = await member_status(chat_id, query.from_user.id)
    if user_status:
        new_order = await order.order_to_be_executed(query.from_user.id, 'group')
        await state.update_data(order_info=new_order)
        if new_order is not None:
            markup = InlineKeyboardBuilder()
            markup.row(types.InlineKeyboardButton(text='Выполнить', callback_data=new_order['link']))
            markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='group_verify'))
            markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='group_next'))
            markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
        else:
            await query.message.answer("Задания закончились")
    else:
        await query.answer("Ошибка! Вы не подписались на канал")


"******************************************************* POST ********************************************************"


@router.callback_query(lambda call: 'executor' in call.data and 'post' in call.data or 'post_next' in call.data)
async def post(query: types.CallbackQuery, state: FSMContext):
    new_order = await order.order_to_be_executed(query.from_user.id, 'post')
    if new_order is not None:
        markup = InlineKeyboardBuilder()
        markup.row(types.InlineKeyboardButton(text='Выполнить', callback_data=new_order['link']))
        markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='post_verify'))
        markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='post_next'))
        markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
    else:
        await query.message.answer("Задания закончились")



@router.callback_query(lambda call: 'executor' in call.data and 'post_verify' in call.data)
async def post_verify(query: types.CallbackQuery, state: FSMContext):
    pass


"*************************************************** OTHER_TASK *******************************************************"


@router.callback_query(lambda call: 'executor' in call.data and 'other_task' in call.data or 'other_task_next' in call.data)
async def other_task(query: types.CallbackQuery, state: FSMContext):
    new_order = await order.order_to_be_executed(query.from_user.id, 'other_task')
    if new_order is not None:
        markup = InlineKeyboardBuilder()
        markup.row(types.InlineKeyboardButton(text='Выполнить', callback_data=new_order['link']))
        markup.row(types.InlineKeyboardButton(text='Проверить', callback_data='other_task_verify'))
        markup.row(types.InlineKeyboardButton(text='Пропустить', callback_data='other_task_next'))
        markup.row(types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
    else:
        await query.message.answer("Задания закончились")


@router.callback_query(lambda call: 'executor' in call.data and 'other_task_verify' in call.data)
async def other_task_verify(query: types.CallbackQuery, state: FSMContext):
    pass
