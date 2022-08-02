from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards import client_kb as ck
router = Router()


class FSMOrder(StatesGroup):
    amount = State()
    price = State()
    urlzadanie = State()
    done = State()

@router.callback_query(lambda call: 'customer' in call.data, state = Customer)
async def order_start(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(FSMOrder.amount)
    await query.message.reply('Вы выбрали реакции')
    await query.message.answer(f'Введите количество')

@router.message(state=FSMOrder.amount)
async def load_amount(message: types.Message, state: FSMContext):
    #Принимаем и записываем данные
    await state.set_state(FSMOrder.price)
    await message.answer('Введите стоимость')

@router.message(state=FSMOrder.price)
async def load_price(message: types.Message, state: FSMContext):
    #Принимаем и записываем данные
    await state.set_state(FSMOrder.urlzadanie)
    await message.answer(f'Вставьте ссылку на чат/сообщение: ')

@router.message(state=FSMOrder.urlzadanie)
async def load_url(message: types.Message, state: FSMContext):
    #Прнимаем и записываем данные
    await state.set_state(FSMOrder.done)
    markup = ReplyKeyboardBuilder()
    markup.row(types.KeyboardButton(text='Отменить'), types.KeyboardButton(text='Подтвердить'))
    await message.answer(f'Вы хотите заказать рекламу для\n\nКоличество: (ЦИФЕРКА)\n\n Стоимость рекламы: \
    (тут ебать считать надо)\n\nКоммисия бота: 100%\n\nОбщая стоимость услуги: ЕБАТЬ ДОХУЯ', reply_markup=markup.as_markup(resize_keyboard=True))

@router.message((F.text == 'Подтвердить'), state=FSMOrder.done)
async def load_done(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Заказ успешно создан!\n\nВы можете следить за прогрессом в своём кабинете!')

@router.message((F.text == 'Отменить'), state=FSMOrder.done)
async def load_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Заказ отменен!')

@router.message(state=FSMOrder.done)
async def another(message: types.Message):
    await message.answer(f'Я не понимаю Вас, выберите либо Отменить, либо Подтвердить!')
