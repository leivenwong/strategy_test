import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from strategy_settings import Settings
import strategy_functions as fuc
from result import Result


def macd_strategy(data_close, ai_settings, result_show, mid, long, short):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute condition
    macd = fuc.compute_macd(data_close, short, long, mid)
    for i in range(len(data_close)):
        if macd[i] >= 0:
            direction[i] = 1
        elif macd[i] < 0 and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction


def macd_ema_strategy(data_close, ai_settings, result_show, short, long):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute condition
    macd = fuc.compute_macd(data_close, 12, 26, 9)
    ema_short = fuc.compute_ema(data_close,short)
    ema_long = fuc.compute_ema(data_close,long)
    for i in range(len(data_close)):
        if macd[i] >= 0 and ema_short[i] > ema_long[i] \
            and ema_long[i] > ema_long[i - 1]:
            direction[i] = 1
        elif macd[i] < 0 and ema_short[i] < ema_long[i] and \
            ema_long[i] < ema_long[i - 1] and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction