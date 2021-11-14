import json
import numpy as np
from ta.volatility import AverageTrueRange
from ta.momentum import rsi
from ta.volume import ChaikinMoneyFlowIndicator
from django.contrib.staticfiles.storage import staticfiles_storage


def addIndicators(df):
    # Add Relative Strength Index (RSI) indicator (Momentum)
    df["rsi"] = rsi(close=df["Close"], window=14, fillna=True)

    # Add Average True Range indicator (Volatility)
    df["atr"] = AverageTrueRange(high=df["High"], low=df["Low"], close=df["Close"], window=14,
                                 fillna=True).average_true_range()

    # Add On-balance Volume indicator (Volume)
    df["cmf"] = ChaikinMoneyFlowIndicator(high=df["High"], low=df["Low"], close=df["Close"], volume=df["Volume"],  window=20, fillna=True).chaikin_money_flow()

    return df

def normalizing(df, symbol):
    minmax = staticfiles_storage.path('minmax_data.json')
    f = open(minmax)
    data = json.load(f)
    # Logging and Differencing
    df['natr'] = df['atr'] / df['Close']
    df['rsi'] = df['rsi'] / 100
    df['Close'] = np.log(df['Close']) - np.log(df['Close'].shift(1))
    # Min Max Scaler implemented
    min = data[symbol+'USDT']['min']
    max = data[symbol+'USDT']['max']
    df['Close'] = (df['Close'] - min) / (max - min)
    df = df[['Close', 'rsi', 'cmf', 'natr']]

    return df
