import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky

from settings import Settings
import functions as fuc
from result import Result
import strategy

#initiate settings
ai_settings = Settings()
result_show = Result()
result_show.reset_net_value()

#read raw data
target = fuc.read_sql(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_format(data_date)

#initiate parameters
short_begin = 3
short_end = 11
long_begin = 20
long_end = 61
cub = (short_end - short_begin) * (long_end - long_begin)
out_net_value = [0] * cub
out_max_retracement = [0] * cub
out_short = [0] * cub
out_long = [0] * cub
test_mark = 0

#start main cycle
for n in range(long_begin, long_end):
    long = n
    for i in range(short_begin, short_end):
        # fetch direction from strategy
        short = i
        direction = strategy.macd_strategy(data_close, result_show, short, long)

        # compute result of strategy
        net_value = fuc.compute_net_value(data_close, direction, ai_settings,
            result_show)
        max_retracement = result_show.max_retracement

        # update result class
        result_show.update_net_value(net_value[-1])
        out_net_value[test_mark] = net_value[-1]
        out_max_retracement[test_mark] = max_retracement
        out_short[test_mark] = i
        out_long[test_mark] = n
        print(str(test_mark)+" of "+str(cub))
        test_mark = test_mark + 1

#print result
print(out_short)
print(out_long)
print(out_net_value)
print(out_max_retracement)

out = pd.DataFrame()
out['short'] = out_short
out['long'] = out_long
out['net_value'] = out_net_value
out['max_retracement'] = out_max_retracement
print(out)

out.to_excel('learning_out.xlsx', 'Sheet1')