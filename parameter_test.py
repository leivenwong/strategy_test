import pandas as pd
import numpy

from strategy_settings import Settings
import strategy_functions as fuc
from result import Result
import strategy
import sys
sys.path.append('D:\\python_project\\statistics')
from statistics_functions import compute_r

#initiate settings
ai_settings = Settings()
result_show = Result()
result_show.reset_net_value()

#read raw data
target = fuc.read_sql_merged(ai_settings)
target = pd.DataFrame(target)

#select close price for compute
data_close = target.loc[0:, ai_settings.fetch_close]
data_open = target.loc[0:, ai_settings.fetch_open]
data_high = target.loc[0:, ai_settings.fetch_high]
data_low = target.loc[0:, ai_settings.fetch_low]
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_format(data_date)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_easy_net(data_close, result_show)

#initiate parameters
step_1 = 0.01
step_2 = 0.001
short_begin = 0.01
short_end = 0.2
long_begin = 0.005
long_end = 0.03
cub = int(((short_end - short_begin) / step_1) *
    ((long_end - long_begin) / step_2))
out_net_value = []
out_max_retracement = []
out_sharp = []
out_short = []
out_long = []
out_r = []
out_success_rate = []
out_profit_loss_rate = []
test_mark = 0

#start main cycle
for n in numpy.arange(long_begin, long_end, step_2):
    long = n
    ai_settings.stop = long
    for i in numpy.arange(short_begin, short_end, step_1):
        print("Parameter " + str(test_mark) + " of " + str(cub))
        # fetch direction from strategy
        short = i
        direction = strategy.macd_ema_strategy(data_close, ai_settings, 9, 26)
        direction_mix = strategy.high_low_strategy(data_close, data_low,
            data_high, ai_settings, short)
        direction_final = fuc.direction_mix(direction, direction_mix)
        direction = direction_final

        # compute result of strategy
        net_value = fuc.compute_net_value(data_close, data_open, data_low,
            data_high, direction, ai_settings, result_show)
        max_retracement = result_show.max_retracement
        std = result_show.std

        # update result class
        result_show.update_net_value(net_value[-1])
        out_net_value.append(net_value[-1])
        out_max_retracement.append(max_retracement)
        out_short.append(i)
        out_long.append(n)
        out_sharp.append(net_value[-1] / std)
        out_r.append(compute_r(target_net_value, net_value))
        out_success_rate.append((result_show.trade_succeed
            / result_show.trade_times))
        out_profit_loss_rate.append(abs(result_show.max_profit
            / result_show.max_loss))
        test_mark = test_mark + 1


#print result and ourput result to excel
out = pd.DataFrame()
out['short'] = out_short
out['long'] = out_long
out['net_value'] = out_net_value
out['max_retracement'] = out_max_retracement
out['success_rate'] = out_success_rate
out['profit_loss_rate'] = out_profit_loss_rate
out['sharp'] = out_sharp
out['r'] = out_r
out.to_excel('learning_out.xlsx', 'Sheet1')

#print result if name is main
if __name__ == '__main__':
    print(out)