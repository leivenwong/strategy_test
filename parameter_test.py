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
data_date = target.loc[0:, ai_settings.fetch_date]
data_date = fuc.date_format(data_date)
target_direction = [1] * len(data_close)
target_net_value = fuc.compute_easy_net(data_close, result_show)

#initiate parameters
short_begin = 0.91
short_end = 1.00
long_begin = 1.01
long_end = 1.09
cub = int(((short_end - short_begin) / 0.01) *
    ((long_end - long_begin) / 0.01 + 1))
out_net_value = [0] * cub
out_max_retracement = [0] * cub
out_sharp = [0] * cub
out_short = [0] * cub
out_long = [0] * cub
out_r = [0] * cub
out_success_rate = [0] * cub
out_profit_loss_rate = [0] * cub
test_mark = 0

#start main cycle
for n in numpy.arange(long_begin, long_end, 0.01):
    long = n
    for i in numpy.arange(short_begin, short_end, 0.01):
        print("Parameter " + str(test_mark) + " of " + str(cub))
        # fetch direction from strategy
        short = i
        direction = strategy.macd_ema_strategy(data_close, ai_settings, 9, 26)
        direction_mix = strategy.far_from_strategy(data_close, ai_settings, 9,
                                                   i, n)
        direction_final = fuc.direction_mix(direction, direction_mix)
        direction = direction_final

        # compute result of strategy
        net_value = fuc.compute_net_value(data_close, direction, ai_settings,
            result_show)
        max_retracement = result_show.max_retracement
        std = result_show.std

        # update result class
        result_show.update_net_value(net_value[-1])
        out_net_value[test_mark] = net_value[-1]
        out_max_retracement[test_mark] = max_retracement
        out_short[test_mark] = i
        out_long[test_mark] = n
        out_sharp[test_mark] = net_value[-1] / std
        out_r[test_mark] = compute_r(target_net_value, net_value)
        out_success_rate[test_mark] = \
            (result_show.trade_succeed / result_show.trade_times)
        out_profit_loss_rate[test_mark] = \
            abs(result_show.max_profit / result_show.max_loss)
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