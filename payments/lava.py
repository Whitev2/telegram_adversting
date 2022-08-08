import requests

from data import Data

data = Data()


class Lava:
    def __init__(self):
        self.database = data.mongo_data()
        self.lava_key = data.lava
        self.lava_wallet = 'R10184401'
        self.headers = {
            'Authorization': self.lava_key
        }

    async def get_connect_status(self):
        url = 'https://api.lava.ru/test/ping'
        params = {
            'account': self.lava_wallet,
        }
        res = requests.get(url, headers=self.headers, params=params)
        return True if res.json()['status'] is True else ValueError("Lawa, Connection refused")

    async def create_withdraw(self,  withdraw_sum: [int, float], withdraw_id: str, wallet_to: str):
        if await self.get_connect_status():
            url = 'https://api.lava.ru/withdraw/create'
            params = {
                'account': self.lava_wallet,
                'amount': float(withdraw_sum),
                'order_id': withdraw_id,
                'success_url': 'https://lava.ru/success',
                'fail_url': 'https://lava.ru/fail',
                'service': 'card',
                'wallet_to': wallet_to

            }
            res = requests.post(url, headers=self.headers, params=params)
            return res.text
        else:
            return {"status": "error", "message": "Lava, Connection refused"}

    async def create_deposit(self, deposit_sum: [int, float], deposit_id: str):
        if await self.get_connect_status():
            url = 'https://api.lava.ru/invoice/create'
            params = {
                'wallet_to': self.lava_wallet,
                'sum': float(deposit_sum),
                'order': deposit_id,
                'success_url': 'https://lava.ru/success',
                'fail_url': 'https://lava.ru/fail',
                'subtract': '1'

            }
            res = requests.post(url, headers=self.headers, params=params)
            return res.url
        else:
            return {"status": "error", "message": "Lava, Connection refused"}

    async def check_deposit_status(self, order_id: str):
        if await self.get_connect_status():
            url = 'https://api.lava.ru/invoice/info'
            params = {
                'order_id': str(order_id)
            }
            res = requests.post(url, headers=self.headers, params=params)
            return res.text
        else:
            return {"status": "error", "message": "Lava, Connection refused"}

    async def check_withdraw_status(self, withdraw_id):
        if await self.get_connect_status():
            url = 'https://api.lava.ru/invoice/info'
            params = {
                'id': str(withdraw_id)
            }
            res = requests.post(url, headers=self.headers, params=params)
            return res.text
        else:
            return {"status": "error", "message": "Lava, Connection refused"}