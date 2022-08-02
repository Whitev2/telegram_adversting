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
