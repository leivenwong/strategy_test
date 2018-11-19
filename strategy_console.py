import pymysql
import pandas as pd

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
#data_date = pd.to_datetime(data_date)
#data_date = fuc.to_date(data_date)

#compute result of target index
target_profit_day = fuc.frofit_per(data_close)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_index_net(data_close, result_show)
target_max_retracement = result_show.easy_max_retracement

# fetch direction from strategy
direction = strategy.macd_ema_strategy(data_close, ai_settings, 9, 26)
direction_mix = strategy.high_low_strategy(data_close, data_low, data_high,
    ai_settings, 0.05)
direction_mix_2 = strategy.rsi_strategy(data_close, ai_settings, 9, 10, 90)
direction_final_pro = fuc.direction_mix(direction, direction_mix)
direction_final = fuc.direction_final(direction_final_pro, direction_mix_2,
    data_date, ai_settings)

# compute result of strategy
transaction = fuc.compute_net_value_not_jump_night(data_close, data_open, data_low,
    data_high, direction_final, ai_settings, result_show)
net_value = list(transaction['net_value'])
print(net_value[-1])