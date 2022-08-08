from datetime import datetime

from aiogram.types import Message

from data import Data
from payments.lava import Lava

data = Data()
lava = Lava()


class Get_info:
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
                           'datetime_come': datetime.now(), 'lg_code': str(lg_code), 'referrals': [],
                           'main_balance': float(0), 'advertising_balance': float(), 'all_time_deposit_advs': float(0),
                           'all_time_main_balance': float(0), 'all_time_withdrawal': float(0), 'main_fines': float(0),
                           'referral_bonus': float(0), 'referral_fines': float(0), 'level': 'Новичек', 'premium': False,
                           'completed_orders_id': [], 'orders_id': []
                           }
            await self.collection_user_info.insert_one(user_answer)
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


class User_balance(Get_info):
    def __init__(self):
        super().__init__()

    async def edit_balance(self, telegram_id: int, balance_type: str, operation: str, edit_sum: float):
        if balance_type.lower() in ('advertising', 'main') and operation.lower() in ('plus', 'minus'):
            user_balance = float()
            if balance_type == 'advertising':
                user_balance = float(await self.get_advertising_balance(telegram_id))
            elif balance_type == 'main':
                user_balance = float(await self.get_main_balance(telegram_id))
            new_balance = float()
            if operation.lower() == 'plus':
                new_balance = user_balance + edit_sum
            elif operation.lower() == 'minus':
                new_balance = user_balance - edit_sum
            try:
                await self.collection_user_info.update_one({'_id': int(telegram_id)}, {'$set': {f'{balance_type.lower()}_balance': float(new_balance)}})
            except Exception as e:
                print(e)
        else:
            ValueError('The type of balance can be "advertising" or "main",'
                       ' only "plus" and "minus" operations are supported')


    async def admin_deposit(self, telegram_id: int,  deposit_sum: float):
        try:
            req = {'_id': int(telegram_id)}, {'$inc': {'advertising_balance': float(deposit_sum)}}
            await self.collection_user_info.update_one(req)
        except Exception as e:
            print(e)

    async def deposit(self, telegram_id, payment_methods,  deposit_sum, deposit_id):
        try:
            if payment_methods == 'Lava':
                lava_deposit = await lava.create_deposit(deposit_sum, deposit_id)
                if lava_deposit['status'] != 'error':
                    req = {'_id': int(telegram_id)}, {'$inc': {'advertising_balance': float(deposit_sum)}}
                    await self.collection_user_info.update_one(req)
                else:
                    return lava_deposit
        except Exception as e:
            print(e)

    async def withdrawal(self, telegram_id: int, payment_methods: str,
                         withdraw_sum: float, withdraw_id: str, wallet_to: str):
        user_info = await self.get_all_info(telegram_id)
        user_main_balance = float(user_info['main_balance'])
        if withdraw_sum <= user_main_balance:
            user_referral_bonus = user_info['referral_bonus']
            user_main_fines = user_info['main_fines']
            user_referral_fines = user_info['referral_fines']
            withdraw = float(withdraw_sum) + float(user_referral_bonus)\
                      - float(user_main_fines) - float(user_referral_fines)
            if withdraw <= user_main_balance:
                try:
                    if payment_methods == 'Lava':
                        lava_withdraw = await lava.create_withdraw(withdraw, withdraw_id, wallet_to)
                        if lava_withdraw['status'] != 'error':
                            await self.edit_balance(telegram_id, 'main', 'minus', withdraw)
                            return {'status': 'success', 'message': 'Withdrawal complete'}
                        else:
                            return lava_withdraw

                except Exception as e:
                    print(e)
            else:
                return {'status': 'error', 'message': 'Withdrawal amount exceeds balance',
                        'main_balance': user_main_balance,
                        'main_fines': user_main_fines,
                        'referral_bonus': user_referral_bonus,
                        'referral_fines': user_referral_fines}
        else:
            return {'status': 'error', 'message': 'Withdrawal amount exceeds balance'}


class Users(User_balance):
    def __init__(self):
        super().__init__()

