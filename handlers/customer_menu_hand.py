from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from data import Data
from orders_info.orders import Order
from keyboards.client_inline import telegram
from keyboards.client_kb import main_menu
from orders_info.user_info import Users
from states.customer_states import Customer

router = Router()
order = Order()
data = Data()
bot = data.get_bot()
router.message.filter(state=Customer)  # После этой строки могут пройти только состояния из Customer
user = Users()

@router.message((F.text == "Телеграм"))
async def info(message: Message):
    await message.answer(f"Какое задание вы хотите заказать?", reply_markup=await telegram(message, 'customer'))


@router.message((F.text == "Другие задания"))
async def info(message: Message):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Создать задание', callback_data='start_other_task'))
    await message.answer(f'Тут вы можете создать любое задание с подробным описанием.\n\n'
                         f'❗️Засчитываться оно будет, только после вашего подтверждения',\
                         reply_markup=markup.as_markup(resize_keyboard=True))


@router.message((F.text == "Назад в меню"))
async def info(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Хорошо, возврат в меню..", reply_markup=await main_menu(message.from_user.id))


@router.message((F.text == "Отменить"), state='*')
async def start_answers(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вы отменили заявку", reply_markup=await main_menu(message))


@router.callback_query(lambda call: 'customer' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    callback = query.data.split()
    await state.update_data(callback=callback)
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Отменить'))
    keyboard = markup.as_markup(resize_keyboard=True)
    if callback[-1] == 'channel':
        await state.update_data(advs_type='channel')
        await state.set_state(Customer.answer_1)
        await query.message.answer(f'Пришлите мне ссылку на канал, на который нужно подписаться', reply_markup=keyboard)
    elif callback[-1] == 'post':
        await state.update_data(advs_type='post')
        await state.set_state(Customer.post_1)
        await query.message.answer(f'Перешлите мне пост, который необходимо смотреть', reply_markup=keyboard)


@router.message(state=Customer.answer_1)
async def start_answers(message: Message, state: FSMContext):
    # проверка есть ли исчточник в списке заданий в процессе или нет

    if '@' in message.text or 'http' in message.text:  # проверка на формат
        await state.set_state()
        await state.update_data(link=message.text)
        await state.set_state(Customer.answer_2)
        await message.answer('Напишите стоимость одного выполнения')
    else:
        await message.answer("Ошибка, введенная ссылка не действительна, повторите попытку")


@router.message(state=Customer.answer_2)
async def start_answers(message: Message, state: FSMContext):
    if float(message.text):
        await state.set_state(Customer.answer_3)
        await state.update_data(click_price=message.text)
        await message.answer('Напишите колличество выполниний')
    else:
        await message.answer("Простите, я принимаю только числа")


@router.message(state=Customer.answer_3)
async def start_answers(message: Message, state: FSMContext):
    amount_people = int(message.text)
    await state.update_data(amount_people=amount_people)
    data = await state.get_data()
    channel_link = data['link']
    click_price = data['click_price']
    summ = amount_people * float(click_price)
    result_sum = summ + (summ / 100 * 2)
    await state.update_data(result_sum=result_sum)
    await state.update_data(order_sum=summ)
    if int(message.text):  # проверка на число
        markup = ReplyKeyboardBuilder()
        markup.row(types.KeyboardButton(text='Отменить'))
        markup.row(types.KeyboardButton(text='Подтвердить'))
        markup.adjust(2)
        await message.answer(f'Вы хотите заказать рекламу для {channel_link}\n\n'
                             f'Количество человек: {message.text}\n'
                             f'Стоимость выполнения: {click_price}р.\n\n'
                             f'Сумма заказа: {round(summ, 2)}р.\n'
                             f'Комиссия 2% от суммы: {round(summ / 100 * 2, 2)}р.\n\n'
                             f'Итого к оплате: {round(result_sum, 2)}р.',
                             reply_markup=markup.as_markup(resize_keyboard=True))
        await state.set_state(Customer.confirm_or_not)
    else:
        await message.answer("Простите, я принимаю только числа")


@router.callback_query(lambda call: call.data == 'start_other_task')
async def add_other_task(query: types.CallbackQuery, state: FSMContext):
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Отменить'))
    await query.message.delete()
    await state.set_state(Customer.link_other_task)
    await query.message.answer(f'Напишите название вашего задания\n\n\nНе более 50 символов!',\
                               reply_markup=markup.as_markup(resize_keyboard=True))

@router.message(state=Customer.link_other_task)
async def link_of_other_task(message: Message, state: FSMContext):
    await state.set_state()
    await state.update_data(name=message.text)
    await state.set_state(Customer.description_other_task)
    await message.answer(f'Введите ссылку на главный источник, где выполнять задание.\n\n\n'
                         f'❗️Ссылка должна начинаться с http:// или https://\n'
                         f'❗️Если ссылок в задании несколько, то укажите остальные в описании.')

@router.message(state=Customer.description_other_task)
async def description_of_other_task(message: Message, state: FSMContext):
    if 'http' in message.text:
        await state.set_state()
        await state.update_data(link=message.text)
        await state.set_state(Customer.count_of_executions_other_task)
        await message.answer(f'Напишите подробное описание')
    else:
        await message.answer("Ошибка, введенная ссылка не действительна, повторите попытку")

@router.message(state=Customer.count_of_executions_other_task)
async def count_of_executions(message: Message, state: FSMContext):
    await state.set_state()
    await state.update_data(description=message.text)
    await state.set_state(Customer.price_other_task)
    await message.answer(f'Введите количество выполнений')

@router.message(state=Customer.price_other_task)
async def price_other_task(message: Message, state: FSMContext):
    if int(message.text):
        await state.set_state()
        await state.update_data(amount_people=int(message.text))
        await state.set_state(Customer.confirm_or_not_other_task)
        await message.answer(f'Введите стоимость одного выполнения')
    else:
        await message.answer("Простите, я принимаю только числа")

@router.message(state=Customer.confirm_or_not_other_task)
async def confirm_or_not_other_task(message: Message, state: FSMContext):
    click_price = float(message.text)
    await state.update_data(click_price=click_price)
    data = await state.get_data()
    name = data['name']
    link = data['link']
    description = data['description']
    amount_people = data['amount_people']
    summ = amount_people * click_price
    result_sum = summ + (summ / 100 * 2)
    await state.update_data(order_sum=result_sum)
    await state.update_data(advs_type='other')
    if float(message.text):
        markup = ReplyKeyboardBuilder()
        markup.row(types.KeyboardButton(text='Отменить'))
        markup.row(types.KeyboardButton(text='Подтвердить'))
        markup.adjust(2)
        await message.answer(f'Название вашего задания: {name}\n\n'
                             f'Вы хотите заказать задание для: {link}\n'
                             f'Описание задания: {description}\n'
                             f'Количество выполнений: {amount_people}\n'
                             f'Стоимость одного выполнения: {click_price}\n\n'
                             f'Сумма заказа: {summ}\n'
                             f'Комиссия бота: 2%\n\n'
                             f'Итого к оплате: {result_sum}',
                             reply_markup=markup.as_markup(resize_keyboard=True))
        await state.set_state(Customer.confirm_or_not)
    else:
        await message.answer("Простите, я принимаю только числа")

@router.message((F.text == "Подтвердить"), state=Customer.confirm_or_not)
async def confirm_pay(message: Message, state: FSMContext):
    user_info = await user.get_all_info(message.from_user.id)
    data = await state.get_data()
    order_sum = data['order_sum']
    advs_type = data['advs_type']
    channel_link = data['link']
    click_price = data['click_price']
    amount_people = data['amount_people']
    user_balance = float(user_info['advertising_balance'])
    result_sum = float(data['order_sum'])
    msg_id = data['msg_id']

    if result_sum <= user_balance and advs_type == 'post':
        await order.new_order(message, advs_type=advs_type, amount_people=amount_people,
                              click_price=click_price, link=msg_id, order_sum=order_sum)
        await message.answer(f'Успешно!\n\nС вашего счёта списано {round(result_sum, 2)}р.'
                             f'\n\nВы можете следить за прогрессом выполнения '
                             f'в своём кабинете', reply_markup=await main_menu(message))

    elif result_sum <= user_balance:
        await order.new_order(message, advs_type=advs_type, amount_people=amount_people,
                              click_price=click_price, link=channel_link, order_sum=order_sum)
        await message.answer(f'Успешно!\n\nС вашего счёта списано {round(result_sum, 2)}р.'
                             f'\n\nВы можете следить за прогрессом выполнения '
                             f'в своём кабинете', reply_markup=await main_menu(message))

    else:
        new_balance = order_sum - user_balance
        markup = InlineKeyboardBuilder()
        markup.button(text='Пополнить баланс', callback_data=f'replenish_the_balance {round(new_balance, 2)}')
        await message.answer(f"К сожалению на вашем счету не хватает {round(order_sum - user_balance, 2)}р."
                             f" для оплаты данной услуги."
                             , reply_markup=await main_menu(message.from_user.id))
        await message.answer(f'Ваш рекламный баланс: {round(user_balance, 2)}', reply_markup=markup.as_markup())

@router.message(state=Customer.post_1)
async def start_answers(message: Message, state: FSMContext):
    message_id = message.message_id
    await state.update_data(message_id=message_id)
    await state.set_state(Customer.post_2)
    await message.answer("Напишите колличество выполнений")

@router.message(state=Customer.post_2)
async def start_answers(message: Message, state: FSMContext):
    amount_people = int(message.text)
    await state.update_data(amount_people=amount_people)
    await state.set_state(Customer.post_3)
    await message.answer("Напишите стоимость просмотра")

@router.message(state=Customer.post_3)
async def start_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']
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
    await state.update_data(advs_type='post')
    await state.update_data(order_sum=result_sum)
    await state.update_data(click_price=click_price)
    await bot.forward_message(chat_id=user_id, from_chat_id=user_id, message_id=message_id)
    await state.set_state(Customer.confirm_or_not)
    await message.answer("Вы хотите создать задачу на просмотр\n\n"
                         f"Количество просмотров: {amount_people}\n"
                         f"Стоимость одного просмотра: {click_price}\n\n"
                         f"Сумма заказа: {order_sum}р.\n"
                         f"Комиссия бота: 2%\n\n"
                         f"Итого к оплате: {result_sum}",
                         reply_markup=markup.as_markup(resize_keyboard=True))




