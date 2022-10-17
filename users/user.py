from datetime import datetime

from aiogram.types import Message

from data import Data

data = Data()


class User:

    def __init__(self):
        self.database = data.mongo_data()
        self.collection_user_info = self.database['user_info']

    async def new_user(self, message: Message):
        t_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        lg_code = message.from_user.language_code

        try:

            user_answer = {'_id': int(t_id), 'username': str(username), 'first_name': str(first_name),
                           'datetime_come': datetime.now(), 'lg_code': str(lg_code), 'referrer': None, 'referrals': [],
                           'main_balance': float(0), 'advertising_balance': float(), 'all_time_deposit_advs': float(0),
                           'all_time_main_balance': float(0), 'all_time_withdrawal': float(0), 'main_fines': float(0),
                           'referral_bonus': float(0), 'referral_fines': float(0), 'level': 'Новичек', 'premium': False,
                           'completed_orders_id': [], 'orders_id': []
                           }
            await self.collection_user_info.insert_one(user_answer)
        except Exception as error:
            print(error)


    async def edit_main_balance(self, telegram_id: int, number: float):
        try:
            request = {'_id': int(telegram_id)}, {'$inc': {'main_balance': float(number)}}
            await self.collection_user_info.replace_one(request)

            if float(number) > float(0):
               await self._all_time_main_balance(telegram_id, number)
            else:
                await self._all_time_withdrawal(telegram_id, number)
        except Exception as error:
            print(error)

    async def edit_advertising_balance(self, telegram_id: int, number: float):
        try:
            request = {'_id': int(telegram_id)}, {'$inc': {'advertising_balance': float(number)}}
            await self.collection_user_info.replace_one(request)

            if float(number) > float(0):
                await self._all_time_deposit_advs(telegram_id, number)
        except Exception as error:
            print(error)


    async def edit_level(self, telegram_id: int, level: str):

        try:
            request = {'_id': int(telegram_id)}, {'level': str(level)}
            if level in ['Новичек', 'Продвинутый', 'Старейшина']:
                await self.collection_user_info.replace_one(request)
            else:
                print('[ERROR]: level not found')
        except Exception as error:
            print(error)

    async def edit_premium(self, telegram_id: int, premium=False):

        try:
            request = {'_id': int(telegram_id)}, {'premium': premium}
            await self.collection_user_info.replace_one(request)
        except Exception as error:
            print(error)

    async def add_completed_order(self, telegram_id: int, order_id: int):
        try:
            request = {'_id': int(telegram_id)}, {'$push:': {'completed_orders_id': order_id}}
            await self.collection_user_info.update_one(request)
        except Exception as error:
            print(error)

    async def add_order(self, telegram_id: int, order_id: int):
        try:
            request = {'_id': int(telegram_id)}, {'$push:': {'orders_id': order_id}}
            await self.collection_user_info.update_one(request)
        except Exception as error:
            print(error)


    async def get_all_info(self, telegram_id):
        user_info = await self.collection_user_info.find_one({'_id': int(telegram_id)})
        return user_info

    async def get_username(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['username']

    async def get_first_name(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['first_name']

    async def get_datetime_come(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['datetime_come']

    async def get_lg_code(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['lg_code']

    async def get_referrals(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['referrals']

    async def get_main_balance(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['main_balance']

    async def get_advertising_balance(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['advertising_balance']

    async def get_all_time_deposit_adersting(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['all_time_deposit_advs']

    async def get_all_time_main_balance(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['all_time_main_balance']

    async def get_all_time_withdrawal(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['all_time_withdrawal']

    async def get_main_fines(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['main_fines']

    async def get_referral_bonus(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['referral_bonus']

    async def get_referral_fines(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['referral_fines']

    async def get_user_level(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['level']

    async def get_premium_status(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['premium']

    async def get_completed_orders_list(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['completed_orders_id']

    async def get_orders_list(self, telegram_id):
        user_info = await self.get_all_info(telegram_id)
        return user_info['orders_id']



    async def _all_time_main_balance(self, telegram_id: int, number: float):
        try:
            request = {'_id': int(telegram_id)}, {'$inc': {'all_time_main_balance': float(number)}}
            await self.collection_user_info.replace_one(request)
        except Exception as error:
            print(error)

    async def _all_time_withdrawal(self, telegram_id: int, number: float):
        try:
            request = {'_id': int(telegram_id)}, {'$inc': {'all_time_withdrawal': float(number)}}
            await self.collection_user_info.replace_one(request)
        except Exception as error:
            print(error)

    async def _all_time_deposit_advs(self, telegram_id: int, number: float):
        try:
            request = {'_id': int(telegram_id)}, {'$inc': {'all_time_withdrawal': float(number)}}
            await self.collection_user_info.replace_one(request)
        except Exception as error:
            print(error)