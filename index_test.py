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

#read raw hs300 data
target = fuc.read_sql(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_left(data_date)

target_profit_day = fuc.frofit_per(data_close)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_net_value(data_close, target_direction)

#compute 5 days ma
ma_5 = fuc.compute_ma(data_close, 5)
ma_10 = fuc.compute_ma(data_close, 10)

#initiate variate
direction = [0] * len(data_close)
trade_times = 0

#compute marks
for i in range(len(data_close)):
    if ma_5[i] >= ma_10[i]:
        direction[i] = 1
    else:
        direction[i] = -1
    if direction[i] != direction[i - 1]:
        trade_times += 1

#compute profit
net_value = fuc.compute_net_value(data_close, direction)

print("Strategy net value: "+str(net_value[-1]))
print("Trade times: "+str(trade_times))
print(ai_settings.fetch_table+" net value: "+str(target_net_value[-1]))

#set window size for plot
plt.figure(dpi=128, figsize=(12, 6))

#set data for plot
plt.subplot(211)
plt.title("Stategy net value",fontsize=12)
plt.plot(net_value, color='Red')

plt.subplot(212)
plt.title(ai_settings.fetch_table+" index net value",fontsize=12)
plt.plot(range(len(data_date)), target_net_value)
plt.xticks(range(len(data_date)), data_date, rotation=0)

#set numbers visible for x lable
fuc.set_xlable_visible(target_net_value)

plt.show()
