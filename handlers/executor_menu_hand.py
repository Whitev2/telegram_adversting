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
from states.executor_states import Executor

router = Router()

router.message.filter(state=Executor)  # После этой строки могут пройти только состояния из Executor


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


@router.callback_query(lambda call: 'executor' in call.data)
async def add_telegram(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer(str(query.data.split()))