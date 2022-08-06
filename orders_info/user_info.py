from data import Data

data = Data()


class User:
    def __init__(self, customer=False, executor=False):
        self.database = data.mongo_data()
        if customer is True and executor is False:
            self.type = 'customer'
            self.collection = self.database['about_the_customer']
        if executor is True and customer is False:
            self.type = 'executor'
            self.collection = self.database['about_the_executor']
        else:
            ValueError('Face type not selected')

    async def get_all_info(self, telegram_id):
        user_info = await self.collection.find_one({'_id': int(telegram_id)})
        return user_info

    async def push_info(self, telegram_id, column_name: str, value):
        await self.collection.update_one({'_id': telegram_id}, {'$push': {column_name: value}})

    async def get_referrals(self, telegram_id) -> list:
        user_info = await self.get_all_info(telegram_id)
        return user_info['referrals']

    async def get_main_balance(self, telegram_id) -> float:
        user_info = await self.get_all_info(telegram_id)
        return user_info['main_balance']

    async def get_referral_balance(self, telegram_id) -> float:
        user_info = await self.get_all_info(telegram_id)
        return user_info['referral_balance']

    async def get_level(self, telegram_id) -> str:
        user_info = await self.get_all_info(telegram_id)
        return user_info['level']

    async def get_premium_status(self, telegram_id) -> bool:
        user_info = await self.get_all_info(telegram_id)
        return user_info['premium']

    async def get_all_time_balance(self, telegram_id) -> float:
        user_info = await self.get_all_info(telegram_id)
        return user_info['all_time_balance']

    async def get_username(self, telegram_id) -> str:
        user_info = await self.get_all_info(telegram_id)
        return user_info['username']

    async def get_first_name(self, telegram_id) -> str:
        user_info = await self.get_all_info(telegram_id)
        return user_info['all_time_balance']

    async def get_datetime_come(self, telegram_id) -> str:
        user_info = await self.get_all_info(telegram_id)
        return user_info['datetime_come']

    async def get_lg_code(self, telegram_id) -> str:
        user_info = await self.get_all_info(telegram_id)
        return user_info['lg_code']

    async def get_orders(self, telegram_id) -> str:
        if self.type == 'customer':
            user_info = await self.get_all_info(telegram_id)
            return user_info['orders']
        else:
            ValueError('Orders for this type cannot be received')

    async def get_completed_orders(self, telegram_id) -> str:
        if self.type == 'executor':
            user_info = await self.get_all_info(telegram_id)
            return user_info['completed_orders']
        else:
            ValueError('Orders for this type cannot be received')

    async def add_complete_order(self, telegram_id, order_id):
        c_name = 'completed_orders'
        await self.push_info(telegram_id, value=int(order_id), column_name=c_name)

    async def top_up_balance(self, t_id, replenishment_amount):
        try:
            await self.collection.update_one({'_id': int(t_id)}, {'$inc': {'main_balance': float(replenishment_amount)}})
        except Exception as e:
            print(e)
