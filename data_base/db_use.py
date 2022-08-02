from datetime import datetime

from aiogram.types import Message

from data import Data

data = Data()

async def about_the_executor(message: Message):
    t_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    lg_code = message.from_user.language_code

    try:
        database = data.mongo_data()
        collection = database['about_the_executor']
        user_answer = {'_id': int(t_id), 'username': str(username), 'first_name': first_name,
                       'datetime_come': datetime.now(), 'lg_code': lg_code, 'referrals': [], 'completed_orders': [],
                       'main_balance': int(0), 'referral_balance': int(0), 'main_fines': int(0),
                       'referral_fines': int(0), 'level': 'новичок', 'API_telegram': [], 'premium': False
                       }
        await collection.insert_one(user_answer)
    except Exception as error:
        print(error)


async def about_the_customer(message: Message):
    t_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    lg_code = message.from_user.language_code

    try:
        database = data.mongo_data()
        collection = database['about_the_customer']
        user_answer = {'_id': int(t_id), 'username': str(username), 'first_name': first_name,
                       'datetime_come': datetime.now(), 'lg_code': lg_code, 'referrals': [], 'orders': [],
                       'main_balance': int(0), 'referral_balance': int(0), 'referral_fines': int(0), 'level': 'новичок'}
        await collection.insert_one(user_answer)
    except Exception as error:
        print(error)