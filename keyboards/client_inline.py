from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def telegram(message: Message, role: str):
    if role in ('executor', 'customer'):
        user_id = message.from_user.id
        markup = InlineKeyboardBuilder()
        markup.button(text='Канал', callback_data=f'{role} {user_id} channel')
        markup.button(text='Пост', callback_data=f'{role} {user_id} post')
        if role == 'executor':
            markup.button(text='Все подряд', callback_data=f'{role} {user_id} all')
        markup.adjust(2)
        return markup.as_markup()
    else:
        print('ERROR')


def profile_menu():
    markup = InlineKeyboardBuilder()
    markup.button(text='Пополнить/вывести', callback_data=f'deposit/withdraw')
    markup.button(text='Пригласить друга', callback_data=f'get_invite_url')
    markup.button(text='Добавить аккаунт', callback_data=f'new_API')
    markup.button(text='История', callback_data=f'history')
    markup.button(text='Премиум', callback_data=f'buy_premium')
    markup.adjust(1, 1, 1, 2)
    return markup.as_markup()


