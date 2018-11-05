import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy
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
data_open = target.loc[0:, ai_settings.fetch_open]
data_high = target.loc[0:, ai_settings.fetch_high]
data_low = target.loc[0:, ai_settings.fetch_low]
data_close = target.loc[0:, ai_settings.fetch_close]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = pd.to_datetime(data_date)
data_date = fuc.to_date(data_date)

ema = fuc.compute_ema(data_close, 9)
macd = fuc.compute_macd(data_close, 12, 26, 9)
rsi = fuc.compute_rsi(data_close, 9)

out = pd.DataFrame()
out['date'] = data_date
out['ema'] = ema
out['macd'] = macd
out['rsi'] = rsi

out.to_excel('indicater_test.xlsx', 'Sheet1')
print(out)