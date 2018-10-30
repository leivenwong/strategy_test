import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from strategy_settings import Settings
import strategy_functions as fuc
from result import Result


def macd_strategy(data_close, ai_settings, mid, long, short):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)
    # compute condition
    macd = fuc.compute_macd(data_close, short, long, mid)
    for i in range(len(data_close)):
        if macd[i] >= 0:
            direction[i] = 1
        elif macd[i] < 0 and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
    return direction


def macd_ema_strategy(data_close, ai_settings, short, long):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    open = 0
    # compute condition
    macd = fuc.compute_macd(data_close, 12, 26, 9)
    ema_short = fuc.compute_ema(data_close,short)
    ema_long = fuc.compute_ema(data_close,long)
    roll = 1
    for i in range(roll, len(data_close)):
        if macd[i - roll] >= 0 and ema_short[i - roll] > ema_long[i - roll] \
        and ema_long[i - roll] > ema_long[i - roll - 1]:
            direction[i] = 1
        elif macd[i - roll] < 0 and ema_short[i - roll] < ema_long[i - roll] and \
        ema_long[i - roll] < ema_long[i - roll - 1] and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
    return direction


def future_strategy(data):
    direction = [0] * len(data)
    for i in range(len(data)-1):
        if data[i + 1] > data[i]:
            direction[i] = 1
        elif data[i + 1] < data[i]:
            direction[i] = -1
        else:
            direction[i] = 0
    return direction


def ema_strategy(data_close, ai_settings, long):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)

    # compute condition
    ema = fuc.compute_ema(data_close,long)
    roll = 1
    for i in range(roll, len(data_close)):
        if ema[i - roll] < ema[i]:
            direction[i] = 1
        elif ema[i - roll] > ema[i] and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
    return direction


def go_with_strategy(data_open, data_close, ai_settings):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)

    # compute condition
    roll = 1
    for i in range(roll, len(data_close)):
        if data_open[i] < data_close[i]:
            direction[i] = 1
        elif data_open[i] > data_close[i] \
            and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
    return direction


def far_from_strategy(data_close, ai_settings, cycle, down_far, up_far):
    print("get strategy...")
    # initiate variate
    direction = [0] * len(data_close)
    ema = fuc.compute_ema(data_close, cycle)

    # compute condition
    for i in range(len(data_close)):
        if data_close[i] / ema[i] < down_far:
            direction[i] = 1
        elif data_close[i] / ema[i] > up_far and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 'follow'
    return direction