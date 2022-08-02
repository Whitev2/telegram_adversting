import asyncio
from datetime import datetime
from aiogram import Dispatcher
from aiogram.client.session import aiohttp
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from data import Data

from handlers import start_hand, customer_menu_hand, executor_menu_hand

data = Data()

bot = data.get_bot()
dp = Dispatcher()


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")

    dp.include_router(start_hand.router)
    dp.include_router(customer_menu_hand.router)
    dp.include_router(executor_menu_hand.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
