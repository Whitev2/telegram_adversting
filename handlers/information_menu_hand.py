from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from keyboards.infobot_inline import info_menu
from states.question_states import Question
from main import bot

router = Router()

@router.callback_query(lambda call: call.data == 'close')
async def close(query: types.CallbackQuery):
    await query.message.delete()

@router.callback_query(lambda call: call.data == 'back')
async def back(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer(f"Информация о боте:", reply_markup=info_menu())

@router.callback_query(lambda call: call.data == 'top_exe')
async def top_executors(query: types.CallbackQuery):
    await query.message.delete()
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Зачем это нужно?', callback_data='for_what'))
    markup.row(types.InlineKeyboardButton(text='Назад', callback_data='back'))
    await query.message.answer(f'Топ 5 исполнителей за неделю:\n\n1.[[ИЗ БД]]\n2.[[ИЗ БД]]\n3.[[ИЗ БД]]\
    \n4.[[ИЗ БД]]\n5.[[ИЗ БД]]\n--------------------\nТоп 2 исполнителя за сутки:\n\n1.[[ИЗ БД]]\n2.[[ИЗ БД]]\
    \n3.[[ИЗ БД]]', reply_markup=markup.as_markup(resize_keyboard=True))

@router.callback_query(lambda call: call.data == 'for_what')
async def for_what(query: types.CallbackQuery):
    await query.message.delete()
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Назад', callback_data='top_exe'))
    await query.message.answer(f'Преимущества для лучших исполнителей:\n\n⭐️Участвуют в еженедельном розыгрыше.\
    \n⭐️Еще что-то\n⭐️Еще что-то\n⭐️Еще что-то\n⭐️Еще что-то', reply_markup=markup.as_markup(resize_keyboard=True))

@router.callback_query(lambda call: call.data == 'dev')
async def dev(query: types.CallbackQuery):
    await query.message.delete()
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Назад', callback_data='back'))
    await query.message.answer(f'Разработчики:\n👨‍💻 @X_0x69\nИ чуть-чуть\n👨‍💻@xyzMoore ',\
                               reply_markup=markup.as_markup(resize_keyboard=True))

@router.callback_query(lambda call: call.data == 'question_from_user')
async def question_from_user(query: types.CallbackQuery):
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Да', callback_data='confirm_question'),\
               types.InlineKeyboardButton(text='Нет', callback_data='back'))
    await query.message.delete()
    await query.message.answer(f'Вы хотите задать вопрос Техподдержке?', reply_markup=markup.as_markup(resize_keyboard=True))

@router.callback_query(lambda call: call.data =='confirm_question')
async def question_confirm(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(Question.question_start)
    await query.message.answer(f'Введите ваш вопрос:')

@router.message(state=Question.question_start)
async def send_to_support(message: Message, state: FSMContext):
    m_id = message.message_id
    username = message.from_user.username
    user_id = message.from_user.id
    await state.set_state(Question.question_send)
    await state.update_data(ask=message.text)
    question = message.text
    markup = InlineKeyboardBuilder()
    markup.row(types.InlineKeyboardButton(text='Ответить', callback_data=f'question_to_support {m_id} {user_id}'))
    await bot.send_message(chat_id='-1001684049768', text=f'Пришел новый вопрос от пользователя!\n@{username}\n{question}',\
                        reply_markup=markup.as_markup(resize_keyboard=True))
    await message.answer(f'Ваш вопрос отправлен!')

@router.callback_query(lambda call: 'question_to_support' in call.data)
async def answer_for_user(query: types.CallbackQuery, state: FSMContext):
    await query.message.reply(f'Введите ответ для пользователя:')
    data = query.data.split()
    await state.update_data(question_user_id=data)
    await state.set_state(Question.answer_for_user)

@router.message(state=Question.answer_for_user)
async def get_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['question_user_id'][-1]
    user_answer = data['question_user_id']
    m_id = user_answer[1]
    try:
        await bot.send_message(chat_id=user_id, text=f'Вам пришел ответ на ваш вопрос✅\n'
                                                     f'Ответ: {message.text}', reply_to_message_id=int(m_id))
    except TelegramBadRequest:
        await bot.send_message(chat_id=user_id, text=f'Вам пришел ответ на ваш вопрос✅\n'
                                                     f'Ответ: {message.text}')


