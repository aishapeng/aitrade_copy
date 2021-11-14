import requests
import pandas as pd
from binance.client import Client


def get_balances(api_key, secret_key):
    try:
        client = Client(api_key, secret_key)
        result = client.get_account()
        balances = {}

        for currency in result['balances']:
            name = currency['asset'].upper().replace("LD", "")
            value = float(currency['free'])

            if value > 0.00001:
                balances[name] = value
        return balances

    except:
        return 0


def get_kline(symbol='BTC'):
    endpoint = "https://api.binance.com/api/v3/klines?symbol=" + symbol + "USDT&interval=1h"
    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    df = df.iloc[:, :5]
    df[0] = df[0].map(lambda x: int(x/1000))
    df.columns = ['time', 'open', 'high', 'low', 'close']
    json = df.to_json(orient='records')
    return json

