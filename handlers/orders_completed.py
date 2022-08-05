from datetime import datetime
from data import Data

data = Data()

async def complete(tg_id: int, advs_type: str, order_id: int, order_name: str):
    database = data.mongo_data()
    collection = database['completed_tasks']
    params = {'TG_ID': tg_id, 'advs_type': advs_type, 'order_id': order_id,
              'order_name': order_name, 'datetime_complete': datetime.now()}
    await collection.insert_one(params)
