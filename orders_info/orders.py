import re
from datetime import datetime
import random

from aiogram.types import Message

from data import Data

from orders_info.user_info import User_balance

data = Data()
bot = data.get_bot()

class Order(User_balance):
    def __init__(self):
        super().__init__()
        self.database = data.mongo_data()
        self.collection_order = self.database['orders']
        self.procent = 2

    async def new_order(self, message: Message, link: str, advs_type: str, amount_people: int,
                        click_price: float, order_sum, chat_id, description=None, media_id=None, task_name=None):
        """
        +–––––––––––––––––––––––Necessary––––––––––––––––––––––––––+
        |    This function is needed to create orders.             |
        |    param message - message.from_user                     |
        |    param link - link on source                           |
        |    param order_name - name for wallets (PRIMARY KEY)     |
        |    param advs_type - advertising type                    |
        |                                                          |
        + –––––––––––––––––––––Not necessary–––––––––––––––––––––– +
        |                                                          |
        |    param description - Required for other tasks          |
        |    param media_id - Required for other tasks             |
        |    param title - Required for other tasks                |
        |                                                          |
        +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
        """
        t_id = message.from_user.id
        try:
            count_documents = int(await self.collection_order.count_documents({}))
            print(count_documents)
            if not count_documents:
                count_documents = 0
            params = {'_id': count_documents + 1, 'telegram_ID': int(t_id), 'link': link, 'advs_type': advs_type,
                      'amount_people': amount_people, 'task_sum': order_sum, 'click_price': float(click_price),
                      'task_date': datetime.now(), 'chat_id': chat_id,
                      'amount_completed': 0, 'status': 'process', 'task_description': description,
                      'media_id': media_id, 'task_name': task_name}
            await self.collection_order.insert_one(params)
            edit_sum = float(amount_people) * float(click_price)
            result_summ = order_sum + (order_sum / 100 * self.procent)
            print('new_order', result_summ)
            await self.edit_balance(t_id, 'advertising', 'minus', float(result_summ))
            return True
        except Exception as error:
            print(error)

    async def order_status(self, order_id: int = None):
        """    
        +–––––––––––––––––––––––Necessary––––––––––––––––––––––––––+
        |    This function checks the status of an order           |
        |    Will return true if the order is completed            |
        |                                                          |
        |    param order - name or ID for wallets                  |
        +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
        """

        if order_id is str:
            order_info = await self.collection_order.find_one({"_id": int(order_id)})
            if order_info['status'] != 'completed':
                if int(order_info['amount_people']) == int(order_info['amount_completed']):
                    await self.collection_order.update_one({"order_name": int(order_id)}, {'status': 'completed'})
                    return True
        else:
            print('Error')
        return False

    async def check_order(self, link: str):
        if link:
            order_info = await self.collection_order.find_one({'$and': [{"link": str(link)}, {'status': 'process'}]})
            if order_info is None:
                return True
            else:
                return False
        else:
            print('Error')



    async def update_amount_completed(self, order_id: int):
        """
        +–––––––––––––––––––––––Necessary––––––––––––––––––––––––––+
        |    This function is needed to update completed tasks     |
        |    param order - name or ID for wallets                  |
        +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
        """
        params = {'$inc': {'amount_completed': 1}}
        await self.collection_order.update_one({"_id": int(order_id)}, params)


    async def order_to_be_executed(self, telegram_id: int, advs_type: str):

        complete_orders = await self.get_completed_orders_list(telegram_id)
        async for order in self.collection_order.aggregate(
                [{"$match": {'$and': [{'advs_type': str(advs_type)},
                                      {'status': 'process'}, {'_id': {'$nin': complete_orders}}]}},
                 {"$sample": {"size": 1}}]):
            return order

    async def completed_orders(self, telegram_id: int, advs_type: str, order_id: int, click_price: float):

        collection = self.collection_order['completed_tasks']
        params = {'telegram_ID': int(telegram_id), 'advs_type': advs_type, 'task_ID': order_id,
                  'datetime_complete': datetime.now(), 'click_price': click_price}
        await collection.insert_one(params)

    async def get_order_info(self, order_id_or_link: [int, str]):
        try:
            order_info = await self.collection_order.find_one({'_id': int(order_id_or_link)})
        except:
            order_info = await self.collection_order.find_one({'link': str(order_id_or_link)})
        return order_info
