from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def telegram(message: Message, role: str):
    if role in ('executor', 'customer'):
        user_id = message.from_user.id
        markup = InlineKeyboardBuilder()
        markup.button(text='Канал', callback_data=f'{role} {user_id} channel')
        markup.button(text='Бот', callback_data=f'{role} {user_id} bot')
        markup.button(text='Пост', callback_data=f'{role} {user_id} post')
        markup.button(text='Реакции', callback_data=f'{role} {user_id} reaction')
        if role == 'executor':
            markup.button(text='Все подряд', callback_data=f'{role} {user_id} all')
        markup.adjust(2, 2)
        return markup.as_markup()
    else:
        print('ERROR')