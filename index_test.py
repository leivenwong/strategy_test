import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky

from settings import Settings
import functions as fuc

#initiate settings
ai_settings = Settings()

#read raw data
target = fuc.read_sql(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_format(data_date)

#compute net value of target index
target_profit_day = fuc.frofit_per(data_close)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_net_value(data_close, target_direction, ai_settings)

#compute ma
ma_20 = fuc.compute_ma(data_close, 20)
ma_10 = fuc.compute_ma(data_close, 10)

#initiate variate
direction = [0] * len(data_close)
trade_times = 0

#compute direction
for i in range(len(data_close)):
    if ma_10[i] >= ma_20[i]:
        direction[i] = 1
    else:
        direction[i] = -1
    if direction[i] != direction[i - 1]:
        trade_times += 1

#compute net value of strategy
net_value = fuc.compute_net_value(data_close, direction, ai_settings)

#print result
print("Strategy net value: "+str(net_value[-1]))
print("Trade times: "+str(trade_times))
print(ai_settings.fetch_table+" net value: "+str(target_net_value[-1]))

#draw plot according to settings
if ai_settings.draw_plot:
    fuc.draw_plot(ai_settings, net_value, target_net_value,data_date)