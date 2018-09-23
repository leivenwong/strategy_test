import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky

from strategy_settings import Settings
import strategy_functions as fuc
import result
import strategy

#initiate settings
ai_settings = Settings()
result_show = result.Result()
result_show.reset_net_value()

#read raw data
target = fuc.read_sql(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_format(data_date)

#compute result of target index
target_profit_day = fuc.frofit_per(data_close)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_net_value(data_close, target_direction,
    ai_settings, result_show)
target_max_retracement = result_show.max_retracement

# fetch direction from strategy
direction = strategy.macd_strategy(data_close, result_show, 5, 60)

# compute result of strategy
net_value = fuc.compute_net_value(data_close, direction, ai_settings,result_show)
max_retracement = result_show.max_retracement

# update result class
result_show.update_net_value(net_value[-1])

#print result
print("Strategy net value: "+str(net_value[-1]))
print("Strategy max retracement: "+str(max_retracement))
print("Trade times: "+str(result_show.trade_times))
print(ai_settings.fetch_table+" net value: "+str(target_net_value[-1]))
print(ai_settings.fetch_table+" max retracement: "+str(target_max_retracement))

#draw plot according to settings
if ai_settings.draw_plot:
    fuc.draw_plot(ai_settings, net_value, target_net_value, data_date)

out_net_value = pd.DataFrame()
out_net_value['net_value'] = net_value
#out_net_value.to_excel("D:\\python_project\\statistics\\net_value.xlsx",
    #"Sheet1")