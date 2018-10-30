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
target_1 = fuc.read_file(ai_settings)
target_2 = fuc.read_sql_merged(ai_settings)
target_2['date'] = target_2['utc_string']
date_2 = target_2.loc[0:, 'date']
date_2 = fuc.date_format(date_2)
target_2['date'] = date_2
target_2['date'] = pd.to_datetime(target_2['date'])
target_1 = pd.DataFrame(target_1)
target_2 = pd.DataFrame(target_2)

grouped_data = pd.merge(target_2, target_1, on='date', how='left')
grouped_data = grouped_data.sort_values(by='date')
grouped_data = grouped_data.fillna(method='ffill')
grouped_data = grouped_data.drop_duplicates()

out = pd.DataFrame()
out['utc_string'] = grouped_data['date']
out['close_price'] = grouped_data['close_price']
out['m1-m2'] = grouped_data['m1-m2']

direction = fuc.m1_m2_direction(out)

out['direction'] = direction
out = out[out['utc_string'] > datetime.datetime(1997, 1, 30)]
out = out.reindex(range(len(out)), method='bfill')

if __name__ == '__main__':
    print(out)