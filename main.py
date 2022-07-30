import asyncio

from data import Data
from aiogram import Dispatcher

from handlers import *

data = Data()
bot = data.get_bot()
dp = Dispatcher()


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")

    dp.include_router(start_hand.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
