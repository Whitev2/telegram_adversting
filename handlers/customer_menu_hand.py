import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data_base.db_use import about_the_executor, about_the_customer
from filters.admin_filters import IsAdmin
from keyboards.client_inline import telegram
from keyboards.client_kb import main_menu, exercise_menu
from states.customer_states import Customer

router = Router()

router.message.filter(state=Customer)  # После этой строки могут пройти только состояния из Customer


@router.message((F.text == "Телеграм"))
async def info(message: Message):
    await message.answer(f"Какое задание вы хотите заказать?", reply_markup=await telegram(message, 'customer'))


@router.message((F.text == "Другие задания"))
async def info(message: Message):
    await message.answer(f"Другие задания")


@router.message((F.text == "Назад в меню"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Хорошо, возврат в меню..", reply_markup=await main_menu(message))

@router.callback_query(lambda call: 'customer' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(Customer.start_answers)
    callback = query.data.split()
    await state.update_data(callback=callback)
    ch_name = str()
    if callback[-1] == 'channel':
        await query.message.answer(f'Пришлите мне ссылку на канал, на который нужно подписаться')
    elif callback[-1] == 'bot':
        await query.message.answer(f'Пришлите мне ссылку на бота, которого необходимо пройти')
    elif callback[-1] == 'post':
        await query.message.answer(f'Пришлите мне ссылку на пост, который необходимо посмотреть')
    elif callback[-1] == 'reaction':
        await query.message.answer(f'Пришлите мне ссылку на пост, где необходимо оставить реакцию')


@router.message(state=Customer.start_answers)
async def start_answers(message: Message, state: FSMContext):
    # проверка есть ли исчточник в списке заданий в процессе или нет

    if '@' in message.text or 'http' in message.text: # проверка на формат
        await state.set_state()
        await state.update_data(answer_1=message.text)
        await state.set_state(Customer.answer_2)
        await message.answer('Напишите стоимость одного выполнения')
    else:
        await message.answer("Ошибка, введенная ссылка не действительна, повторите попытку")


@router.message(state=Customer.answer_2)
async def start_answers(message: Message, state: FSMContext):
    if float(message.text):
        await state.set_state(Customer.answer_3)
        await state.update_data(answer_2=message.text)
        await message.answer('Напишите колличество выполниний')
    else:
        await message.answer("Простите, я принимаю только числа")


@router.message(state=Customer.answer_3)
async def start_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    channel_name = data['answer_1']
    click_price = data['answer_2']
    summ = int(message.text)*float(click_price)
    if int(message.text):  # проверка на число
        markup = ReplyKeyboardBuilder()
        markup.row(types.KeyboardButton(text='Отменить'))
        markup.row(types.KeyboardButton(text='Подтвердить'))
        markup.adjust(2)
        await state.update_data(answer_2=message.text)
        await message.answer(f'Вы хотите заказать рекламу для {channel_name}\n\n'
                             f'Колличество человек: {message.text}\n'
                             f'Стоимость выполнения: {click_price}\n\n'
                             f'Сумма заказа: {summ}\n'
                             f'Комиссия 2% от суммы: {summ/100*2}\n\n'
                             f'Итого к оплате: {summ+(summ/100*2)}', reply_markup=markup.as_markup(resize_keyboar=True))
    else:
        await message.answer("Простите, я принимаю только числа")