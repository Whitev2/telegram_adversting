import os

import psycopg2
from aiogram import Bot


class Data:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.mg_user = os.getenv('MONGO_USER')
        self.mg_pswd = os.getenv('MONGO_PASSWORD')
        self.mg_host = os.getenv('MONGO_HOST')
        self.mg_port = os.getenv('MONGO_PORT')
        self.super_admins = []
        self.THROTTLE_TIME = 0.8
        self.commichannel = os.getenv('COMMIT_CH')
        self.masterchannel = os.getenv('MASTER_CH')
# фывфывфдв
    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")

    def get_postg(self):
        return psycopg2.connect(database=self.pg_db, user=self.pg_user, password=self.pg_pswd, host=self.pg_host, port=int(self.pg_port))

    def get_mongo(self):
        return motor.motor_asyncio.AsyncIOMotorClient(username=self.mg_user, password=self.mg_pswd, host=self.mg_host, port=int(self.mg_port))