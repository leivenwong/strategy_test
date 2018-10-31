import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky
import datetime
import time

from strategy_settings import Settings
import strategy_functions as fuc
import result
import strategy
import sys
sys.path.append('D:\\python_project\\statistics')
from statistics_functions import compute_r

#initiate settings
ai_settings = Settings()
result_show = result.Result()
result_show.reset_net_value()

#read raw data
target = fuc.read_sql_merged(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_open = target.loc[0:, ai_settings.fetch_open]
data_high = target.loc[0:, ai_settings.fetch_high]
data_low = target.loc[0:, ai_settings.fetch_low]
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = pd.to_datetime(data_date)
data_date = fuc.to_date(data_date)

#compute result of target index
target_profit_day = fuc.frofit_per(data_close)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_easy_net(data_close, result_show)
target_max_retracement = result_show.easy_max_retracement

# fetch direction from strategy
direction = strategy.macd_ema_strategy(data_close, ai_settings, 9, 26)
direction_mix = strategy.rsi_strategy(data_close, ai_settings, 9, 20, 80)
direction_final = fuc.direction_mix(direction, direction_mix)

# compute result of strategy
net_value = fuc.compute_net_value(data_close, data_open, data_low, data_high,
    direction_final, ai_settings, result_show)
max_retracement = result_show.max_retracement
r = compute_r(net_value,target_net_value)

# update result class
result_show.update_net_value(net_value[-1])

#print result if name is main
if __name__ == '__main__':
    # print result
    print("Strategy net value: " + str(net_value[-1]))
    print("Strategy R/Y: " + str( -1 + net_value[-1] **
        (1/(len(data_close) / 250))))
    print("Strategy max retracement: " + str(max_retracement))
    print("Trade times: " + str(result_show.trade_times))
    print("Trade succeed: " + str(result_show.trade_succeed))
    print("Trade stopped: " + str(result_show.stop_times))
    print("Trade success rate: " + str(result_show.trade_succeed
                                       / result_show.trade_times))
    print("Max profit: " + str(result_show.max_profit))
    print("Max_loss: " + str(result_show.max_loss))
    print("Profit/risk rate: " + str(abs(result_show.max_profit /
                                         result_show.max_loss)))
    print("Index net value: " + str(target_net_value[-1]))
    print("Index max retracement: " + str(target_max_retracement))
    print("Correlation r: " + str(r))
    out = pd.DataFrame()
    out['date'] = data_date
    out['direction'] = direction_final
    out['net_value'] = net_value
    out['index_net_value'] = target_net_value

    if len(data_close) < 20000:
        print("writting excel...")
        out.to_excel('backtesting.xlsx', 'Sheet1')

#show plot if settings is true
if ai_settings.draw_plot and __name__ == '__main__' \
        and len(data_close) < 20000:
    fuc.draw_plot(ai_settings, net_value, target_net_value, data_date)


