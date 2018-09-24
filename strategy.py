import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from strategy_settings import Settings
import strategy_functions as fuc
from result import Result


def macd_strategy(data_close, ai_settings, result_show, short, long):
    # initiate variate
    direction = [0] * len(data_close)
    trade_times = 0
    # compute condition
    macd = fuc.compute_macd(data_close, 12, 26, 9)
    ema_1 = fuc.compute_ema(data_close, short)
    ema_2 = fuc.compute_ema(data_close, long)
    ema_slope = fuc.compute_ema(data_close,long)
    for i in range(len(data_close)):
        if macd[i] >= 0 and ema_1[i] > ema_2[i] and ema_slope[i] > ema_slope[i - 1]:
            direction[i] = 1
        elif macd[i] < 0 and ema_1[i] < ema_2[i] and ema_slope[i] <= \
                ema_slope[i - 1] and ai_settings.only_buy == False:
            direction[i] = -1
        else:
            direction[i] = 0
        if direction[i] != direction[i - 1]:
            trade_times += 1
    result_show.trade_times = trade_times
    return direction