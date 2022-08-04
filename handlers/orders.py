from datetime import datetime

from aiogram.types import Message

from data import Data

data = Data()


class Order:
    def __init__(self):
        self.database = data.mongo_data()
        self.collection = self.database['orders']

    async def new_order(self, message: Message, link: str, advs_type: str, amount_people: int,
                        click_price: float, description=None, media_id=None, title=None):
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
            count_documents = int(await self.collection.count_documents({}))
            print(count_documents)
            if not count_documents:
                count_documents = 0
            params = {'_id': count_documents + 1, 'telegram_ID': int(t_id), 'link': link,
                      'order_name': f'order_{count_documents + 1}', 'advs_type': advs_type,
                      'amount_people': amount_people, 'click_price': float(click_price), 'order_date': datetime.now(),
                      'amount_completed': 0, 'status': 'process', 'description': description,
                      'media_id': media_id, 'title': title}
            await self.collection.insert_one(params)
            return True
        except Exception as error:
            print(error)

    async def order_status(self, order: [int, str]):
        """    
        +–––––––––––––––––––––––Necessary––––––––––––––––––––––––––+
        |    This function checks the status of an order           |
        |    Will return true if the order is completed            |
        |                                                          |
        |    param order - name or ID for wallets                  |
        +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
        """

        if order is int:
            order_info = await self.collection.find_one({"_id": int(order)})
            if order['status'] != 'completed':
                if int(order_info['amount_people']) == int(order_info['amount_completed']):
                    await self.collection.update_one({"_id": int(order)}, {'status': 'completed'})
                    return True
            else:
                return True

        elif order is str:
            order_info = await self.collection.find_one({"order_name": str(order)})
            if order['status'] != 'completed':
                if int(order_info['amount_people']) == int(order_info['amount_completed']):
                    await self.collection.update_one({"order_name": str(order)}, {'status': 'completed'})
                    return True
            else:
                return True
        else:
            print('Error')
        return False

    async def update_amount_completed(self, order: [int, str]):
        """
        +–––––––––––––––––––––––Necessary––––––––––––––––––––––––––+
        |    This function is needed to update completed tasks     |
        |    param order - name or ID for wallets                  |
        +––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+
        """
        params = {'$inc': {'amount_completed': 1}}

        if order is int:
            await self.collection.update_one({"_id": int(order)}, params)
        elif order is str:
            await self.collection.update_one({"order_name": str(order)}, params)
        else:
            print('Error')
