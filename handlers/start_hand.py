import asyncio
from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.filters.command import CommandStart, CommandObject
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()

@router.message(commands=['start', 'help'])
async def start(message: Message):
    await message.answer("Добро пожаловать")