import requests

from data import Data

data = Data()


class Payments():
    def __init__(self):
        self.database = data.mongo_data()
        self.lava_key = data.lava
        self.lava_wallet = 'R10184401'
        self.headers = {
            'Authorization': self.lava_key
        }
    #  local balance
    async def top_up_balance(self, t_id, collection: str, replenishment_amount):
        try:
            coll = self.database[collection]
            await coll.update_one({'_id': int(t_id)}, {'$inc': {'main_balance': int(replenishment_amount)}})
        except Exception as e:
            print(e)

    async def write_off_balance(self, t_id, collection: str, withdrawal_amount):
        pass

    async def local_transaction(self, t_id_sender, collection_sender: str, t_id_recipient, collection_recipient, replenishment_amount):
        pass

    async def fines(self, t_id, collection: str, fines_amount):
        pass

    #  lawa wallet
    async def issue_an_invoice(self, sum, order):
        url = 'https://api.lava.ru/invoice/create'
        params = {
            'wallet_to': self.lava_wallet,
            'sum': sum,
            'order': order,
            'success_url': 'https://lava.ru/success',
            'fail_url': 'https://lava.ru/fail',
            'subtract': '1'

        }
        res = requests.post(url, headers=self.headers, params=params)
        return res.url

    async def check_receipt(self, order):
        url = 'https://api.lava.ru/invoice/info'
        params = {
            'order': order
        }
        res = requests.post(url, headers=self.headers, params=params)
        return res.json()['status']