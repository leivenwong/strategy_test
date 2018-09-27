import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import datetime
import time

from strategy_settings import Settings
from result import Result


def read_sql_merged(ai_settings):
    """read data from sql database"""
    print("Enter Mysql")
    engine = create_engine(ai_settings.sql_path_merged)
    df = pd.read_sql(sql="select * from "+ai_settings.fetch_table, con=engine)
    print("Out Mysql")
    return df

def read_sql_backtesting(ai_settings):
    """read data from sql database"""
    print("Enter Mysql")
    engine = create_engine(ai_settings.sql_path_backtesting)
    df = pd.read_sql(sql="select * from "+ai_settings.fetch_table, con=engine)
    print("Out Mysql")
    return df

def read_file(ai_settings):
    """read data from data_path"""
    ai_settings = Settings()
    file_path = ai_settings.file_path
    loads = pd.read_excel(file_path)
    return loads


def compute_ma(data,cycle):
    """compute ma value list"""
    ma_cycle = list(range(len(data)))
    for i in range(cycle):
        ma_cycle[i] = data[0]
    for i in range(cycle, len(data)):
        ma_cycle[i] = (sum(data[i - cycle:i])) / cycle
    return ma_cycle


def compute_easy_net(data,result_show):
    """compute easy net value for target"""
    print("compute easy net value...")
    net_value = [1] * len(data)
    max_value = 0

    # initiate max retracement
    result_show.easy_max_retracement = 0
    for i in range(len(data)):
        #print("Easy net: "+str(i)+" of "+str(len(data)))

        #compute easy net value
        net_value[i] = data[i] / data[0]

        #update max retracement
        if net_value[i] > max_value:
            max_value = net_value[i]
        retracement = (max_value - net_value[i]) / max_value
        if retracement > result_show.easy_max_retracement:
            result_show.easy_max_retracement = retracement
    print("easy net value compute has completed.")
    return net_value


def compute_net_value(data, direction, ai_setting, result_show):
    """compute net value list"""
    print("begin compute net value...")
    net_value = [0] * len(data)
    net_value[0] = 1
    max_value = 0
    trade_succeed = 0

    # initiate max retracement
    result_show.max_retracement = 0
    for i in range(1, len(data)):
        #print("Net value: "+str(i) + " of " +str(len(data)))

        #compute fees
        if direction[i - 1] != direction[i]:
            fee_mark = ai_setting.trade_fee
        else:
            fee_mark = 0

        #compute trade success times for success rate
        if direction[i - 1] == 0 and direction[i] == 1:
            result_show.open = data[i]
        elif direction[i - 1] == 0 and direction[i] == -1:
            result_show.open = data[i]
        elif direction[i - 1] == 1 and direction[i] == 0:
            result_show.close = data[i]
            if result_show.close > result_show.open:
                trade_succeed += 1
            if (result_show.close - result_show.open) / result_show.open \
                > result_show.max_profit:
                result_show.max_profit = \
                    (result_show.close - result_show.open) / result_show.open
            if (result_show.close -  result_show.open) / result_show.open \
                < result_show.max_loss:
                result_show.max_loss = \
                    (result_show.close - result_show.open) / result_show.open
        elif direction[i - 1] == -1 and direction[i] == 0:
            result_show.close = data[i]
            if result_show.close < result_show.open:
                trade_succeed += 1
            if (result_show.open - result_show.close) / result_show.open \
                > result_show.max_profit:
                result_show.max_profit = \
                    (result_show.open - result_show.close) / result_show.open
            if (result_show.open / result_show.close) / result_show.open \
                < result_show.max_loss:
                result_show.max_loss = \
                    (result_show.open - result_show.close) / result_show.open
        elif direction[i - 1] == -1 and direction[i] == 1:
            result_show.close = data[i]
            if result_show.close < result_show.open:
                trade_succeed += 1
            if (result_show.open - result_show.close) / result_show.open \
                    > result_show.max_profit:
                result_show.max_profit = \
                    (result_show.open - result_show.close) / result_show.open
            if (result_show.open / result_show.close) / result_show.open \
                    < result_show.max_loss:
                result_show.max_loss = \
                    (result_show.open - result_show.close) / result_show.open
            result_show.open = data[i]
        elif direction[i - 1] == 1 and direction[i] == -1:
            result_show.close = data[i]
            if result_show.close > result_show.open:
                trade_succeed += 1
            if (result_show.close - result_show.open) / result_show.open \
                > result_show.max_profit:
                result_show.max_profit = \
                    (result_show.close - result_show.open) / result_show.open
            if (result_show.close - result_show.open) / result_show.open \
                < result_show.max_loss:
                result_show.max_loss = \
                    (result_show.close - result_show.open) / result_show.open
            result_show.open = data[i]

        #compute net value according to strategy direction
        rt = ai_setting.leverage_rate
        if direction[i - 1] == 1:
            net_value[i] = net_value[i - 1] * ((data[i] - data[i - 1]) *
            rt / data[i - 1] + 1 - fee_mark * rt)
        elif direction[i - 1] == -1:
            net_value[i] = net_value[i - 1] * ((data[i - 1] - data[i]) *
            rt / data[i - 1] + 1 - fee_mark * rt)
        else:
            net_value[i] = net_value[i - 1]

        #update max retracement
        if net_value[i] > max_value:
            max_value = net_value[i]
        retracement = (max_value - net_value[i]) / max_value
        if retracement > result_show.max_retracement:
            result_show.max_retracement = retracement

    #update std and trade success times
    result_show.std = compute_std(net_value)
    result_show.trade_succeed = trade_succeed
    print("net value compute has completed.")
    return net_value


def frofit_per(data_close):
    """compute profit rate per day or other cycle"""
    profit_per = list(range(len(data_close)))
    profit_per[0] = 0
    for i in range(1, len(data_close)):
        profit_per[i] = (data_close[i] / data_close[i - 1] - 1) * 100
    return profit_per


def set_xlable_visible(data):
    """set x lable's"visible config"""
    ax = plt.gca()
    visible_count = int(len(data) / 3)
    for ind, label in enumerate(ax.xaxis.get_ticklabels()):
        if ind % visible_count == 0:  # set visible number of x lable
            label.set_visible(True)
        else:
            label.set_visible(False)
        if ind / int(len(data) - 1) == 1:
            label.set_visible(True)
    ax = plt.gca()
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(0)


def date_format(data):
    """set date format which wanted"""
    for i in range(len(data)):
        data[i] = str(data[i])
        data[i] = data[i][0:10]
    return  data


def draw_plot(ai_settings, net_value, target_net_value, data_date):
    print("waiting for plot drawing...")
    # set window size for plot
    plt.figure(dpi=128, figsize=(12, 6))
    # set data for plot
    plt.subplot(211)
    plt.title("Stategy net value", fontsize=12)
    plt.plot(net_value, color='Red')

    plt.subplot(212)
    plt.title(ai_settings.fetch_table + " index net value", fontsize=12)
    plt.plot(range(len(data_date)), target_net_value)
    plt.xticks(range(len(data_date)), data_date, rotation=0)

    # set numbers visible for x lable
    set_xlable_visible(target_net_value)

    plt.show()


def compute_std(data):
    """compute var for data"""
    compute_average = sum(data) / len(data)
    var = list(range(len(data)))
    for n in range(len(data)):
        var[n] = (data[n] - compute_average) ** 2
    compute_var = sum(var) / len(data)
    return compute_var ** (1/2)

def compute_ema(data,cycle):
    ema = [0] * len(data)
    ema[1] = data[1]
    for i in range(2, len(data)):
        ema[i] = (2 * data[i] + (cycle - 1) * ema[i - 1]) / (cycle + 1)
    return (ema)

def compute_macd(data, short, long, mid):
    dif_short = compute_ema(data, short)
    dif_long = compute_ema(data, long)
    dif = list(map(lambda x: x[0]-x[1], zip(dif_short, dif_long)))
    dea = compute_ema(dif, mid)
    macd = list(map(lambda x: x[0]-x[1], zip(dif, dea)))
    macd = [i * 2 for i in macd]
    return macd

def direction_mix(direction, direction_mix):
    direction_final = [0] * len(direction)
    for i in range(len(direction)):
        if direction[i] == 1 and direction_mix[i] == 1:
            direction_final[i] = 1
        elif direction[i] == -1 and direction_mix[i] == -1:
            direction_final[i] = -1
        else:
            direction_final[i] = 0
    return direction_final


def to_date(data):
    data_date = [0] * len(data)
    for i in range(len(data)):
        data_date[i] = datetime.datetime.date(data[i])
    return data_date


def random_int(a, b, times):
    r = [0] * times
    for i in range(times):
        r[i] = rd.randint(a, b)
        print(r[i])
    return r


def m1_m2_direction(out):
    direction = [0] * len(out)
    for mark in range(2, len(out)):
        if out.loc[mark -1, 'm1-m2'] > out.loc[mark - 2, 'm1-m2']:
            direction[mark] = 1
        elif out.loc[mark - 1, 'm1-m2'] < out.loc[mark - 2, 'm1-m2']:
            direction[mark] = -1
        else:
            direction[mark] = direction[mark - 1]
        mark += 1
    return direction


def if_main(net_value):
    if __name__ == '__main__':
        return net_value