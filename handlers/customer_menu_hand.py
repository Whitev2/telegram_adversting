import re

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data import Data
from orders_info.orders import Order
from keyboards.client_inline import telegram
from keyboards.client_kb import main_menu
from orders_info.user_info import Users
from states.customer_states import Customer
from states.new_chat_state import Chat
from tools.chats_check import member_status
from tools.comission import comission, check_comission

router = Router()
order = Order()
data = Data()
bot = data.get_bot()
router.message.filter(state=Customer)  # После этой строки могут пройти только состояния из Customer
user = Users()


@router.message((F.text == "Телеграм"))
async def info(message: Message):
    await message.answer(f"Какое задание вы хотите создать?", reply_markup=await telegram(message, 'customer'))


@router.message((F.text == "Другие задания"))
async def info(message: Message):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Создать задание', callback_data='start_other_task'))
    await message.answer(f'Тут вы можете создать любое задание с подробным описанием.\n\n'
                         f'❗️Засчитываться оно будет, только после вашего подтверждения', \
                         reply_markup=markup.as_markup(resize_keyboard=True))


@router.message((F.text == "Назад в меню"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Хорошо, возврат в меню..", reply_markup=await main_menu(message.from_user.id))


@router.message((F.text == "Отменить"), state='*')
async def start_answers(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вы отменили заявку", reply_markup=await main_menu(message))



@router.callback_query(lambda call: 'customer' in call.data and 'channel' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(advs_type='channel')
    await state.set_state()
    await state.set_state(Customer.amount)
    await query.message.answer(f'Напишите количество выполнений.\n\n\n'
                               f'❗ Минимальное кол-во выполнений: 10\n'
                               f'❗ Принимаются только целые числа')


@router.message(state=Customer.amount)
async def start_answers(message: Message, state: FSMContext):
    rec_price = 0.4
    text = (f'Напишите стоимость одного выполнения.\n\n\n'
            f'✅ Рекомендованная стоимость задания: {rec_price}\n'
            f'❗ Минимальная стоимость выполнения: 0.02\n'
            f'❗ Принимаются только целые числа')
    try:
        if int(message.text) >= 10:
            await state.update_data(amount=int(message.text))
            await state.set_state(Customer.price)
            await message.answer('Ваше задание:\n\n'
                                 f'Кол-во выполнений: {message.text}\n\n\n')
            await message.answer(text)
        else:
            await message.answer("❗ Введенное число меньше 10, пожалуйста повторите попытку.")

    except ValueError:
        await message.answer("❗ Вы ввели не число, пожалуйста повторите попытку.")


@router.message(state=Customer.price)
async def start_answers(message: Message, state: FSMContext):

    text = (f'Напишите ссылку на ваш канал.\n\n\n'
            f'❗ Ссылка должна содержать https://')
    try:
        if len(message.text[message.text.index('.') + 1:]) >= 3:
            await message.answer("❗ Допустимо только два знака после запятой, пожалуйста повторите попытку.")

        elif float(message.text) >= 0.02:
            data = await state.get_data()
            amount = data['amount']
            sum_price = amount * float(message.text)
            result_price = sum_price + await comission(sum_price)
            comission_number = await check_comission()
            await state.update_data(price=float(message.text))
            await state.set_state(Customer.link)
            await message.answer('Ваше задание:\n\n'
                                 f'Кол-во выполнений: {amount}\n'
                                 f'Стоимость одного выполнения: {message.text}р.\n\n'
                                 f'Сумма заказа: {sum_price}\n'
                                 f'Комиссия бота: {comission_number}%\n'
                                 f'Итого к оплате: {result_price}')
            await message.answer(text)
        else:
            await message.answer("❗ Введенное число меньше 0.02, пожалуйста повторите попытку.")

    except ValueError:
        await message.answer("❗ Вы ввели не число, пожалуйста повторите попытку.")

    except Exception as e:
        print(e)


@router.message(state=Customer.link)
async def start_answers(message: Message, state: FSMContext):

    text = (f'Добавьте бота в ваш канал.\n\n\n'
            f'❗ Бот должен иметь права администратора\n'
            f'❗ Нажмите "Проверить" после добавления')
    try:
        if 'https://' in str(message.text) and 't.me' in str(message.text):
            data = await state.get_data()
            amount = data['amount']
            await state.update_data(link=message.text)
 
            await message.answer('Ваше задание:\n\n'
                                 f'Кол-во выполнений: {amount}\n'
                                 f'Стоимость одного выполнения: {message.text}\n'
                                 f'Ссылка: {message.text}')
            await message.answer(text)
        else:
            await message.answer("❗ Неверная ссылка, пожалуйста повторите попытку.")

    except ValueError:
        await message.answer("❗ Ссылка не может быть в виде числа, пожалуйста повторите попытку.")








@router.callback_query(lambda call: 'customer' in call.data and 'group' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(advs_type='group')
    await state.set_state()
    bot_info = await bot.get_me()
    await query.message.answer(f'Напишите количество выполнений.\n\n\n'
                               f'❗ Минимальное кол-во выполнений: 10\n'
                               f'❗ Принимаются только целые числа')

@router.callback_query(lambda call: 'customer' in call.data and 'post' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await state.update_data(advs_type='post')
    await query.message.answer(f'Напишите количество выполнений.\n\n\n'
                               f'❗ Минимальное кол-во выполнений: 10\n'
                               f'❗ Принимаются только целые числа')




























































@router.message(state=Customer.post_1)
async def start_answers(message: Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    await state.set_state(Customer.post_2)
    await message.answer("Напишите колличество выполнений")


@router.message(state=Customer.post_2)
async def start_answers(message: Message, state: FSMContext):
    if int(message.text):
        amount_people = int(message.text)
        await state.update_data(amount_people=amount_people)
        await state.set_state(Customer.post_3)
        await message.answer("Напишите стоимость просмотра")
    else:
        await message.answer("Простите, я принимаю только числа")


@router.message(state=Customer.post_3)
async def start_answers(message: Message, state: FSMContext):
    if float(message.text):
        data = await state.get_data()
        message_id = data['message_id']
        print(message_id)
        print(11111111111)
        amount_people = data['amount_people']
        click_price = float(message.text)
        user_id = message.from_user.id
        order_sum = amount_people * click_price
        result_sum = order_sum + (order_sum / 100 * 2)
        markup = ReplyKeyboardBuilder()
        markup.row(types.KeyboardButton(text='Отменить'))
        markup.row(types.KeyboardButton(text='Подтвердить'))
        markup.adjust(2)
        await state.update_data(msg_id=message_id)
        await state.update_data(name=None)
        await state.update_data(link=None)
        await state.update_data(chat_id=None)
        await state.update_data(advs_type='post')
        await state.update_data(order_sum=result_sum)
        await state.update_data(click_price=click_price)
        await bot.forward_message(chat_id=user_id, from_chat_id=user_id, message_id=message_id)


        await message.answer("Вы хотите создать задачу на просмотр\n\n"
                             f"Количество просмотров: {amount_people}\n"
                             f"Стоимость одного просмотра: {click_price}\n\n"
                             f"Сумма заказа: {order_sum}р.\n"
                             f"Комиссия бота: 2%\n\n"
                             f"Итого к оплате: {result_sum}",
                             reply_markup=markup.as_markup(resize_keyboard=True))


    else:
        await message.answer("Простите, я принимаю только числа")
