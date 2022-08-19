from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from data import Data
from states.customer_states import Customer

from states.new_chat_state import Chat
from tools.chats_check import member_status

router = Router()
router.message.filter(state=Chat.member)

data = Data()
bot = data.get_bot()


@router.my_chat_member()
async def srt_answers(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        channel_id = message.chat.id
        user_status = await member_status(channel_id, user_id)
        if user_status:
            await state.update_data(chat_id=channel_id)
            print(1)
            await state.set_state(Customer.answer_2)
            await bot.send_message(chat_id=user_id, text='Напишите стоимость одного выполнения\n\n\n'
                                                         '❗Допускается два знака после запятой')
        else:
            await bot.send_message('Ошибка, пожалуйства выполните инструкцию строго по порядку')


    except TelegramForbiddenError:
        await bot.send_message(chat_id=user_id, text='Ошибка, проверьте пункты и повторите попытку:\n\n'
                                                     '❕ Бот не был добавлен в канал для рекламы\n'
                                                     '❕ Боту ограничили доступ к сообщениям\n')
    except:
        await bot.send_message(chat_id=user_id, text='На данном этапе вы можете только переслать сообщение из канала')
