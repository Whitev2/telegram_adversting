from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
from data import Data

data = Data()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in data.admins:
            return True
        else:
            return False