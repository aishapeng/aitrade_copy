import requests
import pandas as pd
import numpy as np
from background_task import background
from .models import Cryptocurrency
from account.models import Account
from .model import Actor_Model
from .utils import addIndicators, normalizing
from django.contrib.staticfiles.storage import staticfiles_storage


class Agent:
    def __init__(self, model_path):
        self.actor = Actor_Model()
        self.actor.Actor.load_weights(model_path)

    def act(self, state):
        prediction = self.actor.Actor.predict(np.expand_dims(state, axis=0))[0]
        action = np.argmax(prediction)
        return action


price_list = {}


@background
def save_pnl():
    all_user = Account.objects.all()
    for user in all_user:
        if user.is_admin:
            pass
        user.save_pnl(price_list)


@background
def load_model():
    global agent
    agent = Agent(staticfiles_storage.path('latest_Actor.h5'))


@background
def act():
    all_user = Account.objects.all()
    for user in all_user:
        if user.is_admin:
            pass
        else:
            user.get_trade_quantity()

    all_coin = Cryptocurrency.objects.all()
    for coin in all_coin:
        endpoint = 'https://api.binance.com/api/v3/klines?symbol=' + str(coin) + 'USDT&interval=1h'
        response = requests.get(endpoint)
        json = response.json()
        df = pd.DataFrame(json)
        df = df[-121:]  # additional 21 to discard for indicators & normalizing
        df = df[[1, 2, 3, 4, 5]]
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        price = df.iloc[-1]['Close']
        price_list[str(coin)] = df.iloc[-1]['Close']  # to count pnl
        df = df.apply(pd.to_numeric)
        df = addIndicators(df)
        df = df[20:]  # remove 1st 20 row after indicators
        df = normalizing(df, str(coin))
        df = df[1:]  # remove 1st row after normalize
        state = df.to_numpy()
        action = agent.act(state)
        print(coin, action)

        if action == 0:
            return 0

        for user in all_user:
            if user.is_admin:
                pass
            else:
                user.get_client()
                user.trade(symbol=str(coin), price=price, action=action)
