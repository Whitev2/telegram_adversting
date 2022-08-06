import os
import motor.motor_asyncio
from aiogram import Bot
from redis.utils import from_url


class Data:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.mg_user = os.getenv('MONGO_USER')
        self.mg_pswd = os.getenv('MONGO_PASSWORD')
        self.mg_host = os.getenv('MONGO_HOST')
        self.mg_port = os.getenv('MONGO_PORT')
        self.lava = os.getenv('LAVA_KEY')
        self.admins = [2036190335, 287476216]
        self.THROTTLE_TIME = 0.8

    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")

    def mongo_data(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(username=self.mg_user, password=self.mg_pswd, host=self.mg_host,
                                                        port=int(self.mg_port))
        return client['database']
