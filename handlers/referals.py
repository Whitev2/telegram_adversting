import asyncio
import re

from aiogram.types import Message

from data import Data
from orders_info.user_info import Users

data = Data()
user = Users()


async def advertising_value(tag, message: Message):
    referrer_id = int(tag[::-1])
    referral_id = int(message.from_user.id)
    user_info_referral = await user.get_all_info(referral_id)
    user_info_referrer = await user.get_all_info(referrer_id)
    print(user_info_referrer['referrals'])
    print(user_info_referral['referrer'])
    database = data.mongo_data()
    collection_user_info = database['user_info']

    if referrer_id not in user_info_referrer['referrals'] and referral_id not in user_info_referrer['referrals']:
        await collection_user_info.update_one({'_id': referrer_id}, {'$push': {'referrals': referral_id}})

    if user_info_referral['referrer'] is None and referrer_id != referral_id:
        await collection_user_info.update_one({'_id': referral_id}, {'$set': {'referrer': referrer_id}}, upsert=True)
