import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from settings import Settings
import functions as fuc
from result import Result

def ma_strategy(data_close, result_show):
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute ma
    ma_5 = data_close.rolling(5).mean()
    ma_10 = data_close.rolling(10).mean()
    for i in range(len(data_close)):
        if ma_5[i] >= ma_10[i]:
            direction[i] = 1
        else:
            direction[i] = -1
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction

def ema_strategy(data_close, result_show):
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute ma
    ema_5 = fuc.compute_ema(data_close,5)
    ema_10 = fuc.compute_ema(data_close,10)
    for i in range(len(data_close)):
        if ema_5[i] >= ema_10[i]:
            direction[i] = 1
        else:
            direction[i] = -1
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction

def macd_strategy(data_close, result_show):
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute ma
    macd = fuc.compute_macd(data_close, 12, 26, 9)
    ema_1 = fuc.compute_ema(data_close,8)
    ema_2 = fuc.compute_ema(data_close,13)
    for i in range(len(data_close)):
        if macd[i] >= 0 and ema_1[i] > ema_2[i]:
            direction[i] = 1
        else:
            direction[i] = -1
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction