import re

from data import Data

data = Data()

bot = data.get_bot()


async def member_status(chat_id, telegram_id):
    user_channel_status = await bot.get_chat_member(chat_id=chat_id, user_id=telegram_id)
    status = user_channel_status.status
    user_channel_status = re.findall(r"\w*", str(user_channel_status))
    try:
        if user_channel_status[70] != 'left':
            return True
        else:
            return False
    except:
        if user_channel_status[60] != 'left':
            return True
        else:
            return False
