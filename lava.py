import requests

from data import Data

data = Data()
def lava():
    url = 'https://api.lava.ru/wallet/list'
    headers = {
        'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiI0OGFkZTgyOC0wYmY3LWQ3NzEtYmY5ZC1jNmMxYzY2OTBiMDMiLCJ0aWQiOiJhNzA2Y2I0My02MGRiLTI2ZmEtNTcyZC1lNWU5NDAwNzIzNTQifQ.CniukBunT6CWM5YD4x6wM9FwTpSd3aYTtNE5UGj1_l8'
    }
    params = {
        'wallet_to': 'R10184401',
        'sum': 10.00

    }

    res = requests.get(url, headers=headers, params=params)
    print(res.url)
    print(res.text)