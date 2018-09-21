import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from settings import Settings
from result import Result


def read_sql(ai_settings):
    """read data from sql database"""
    print("Enter Mysql")
    engine = create_engine(ai_settings.sql_path)
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


def compute_net_value(data, direction, ai_setting, result_show):
    """compute net value list"""
    print("begin compute net value...")
    net_value = [0] * len(data)
    net_value[0] = 1
    max_value = 0
    retracement = [0] * len(data)
    for i in range(1, len(data)):
        if direction[i - 1] != direction[i]:
            fee_mark = ai_setting.trade_fee
        else:
            fee_mark = 0
        if direction[i - 1] == 1:
            net_value[i] = net_value[i - 1] * ((data[i] - data[i - 1])
                / data[i - 1] + 1 - fee_mark)
        elif direction[i - 1] == -1:
            net_value[i] = net_value[i - 1] * ((data[i - 1] - data[i])
                / data[i - 1] + 1 - fee_mark)
        else:
            net_value[i] = net_value[i - 1]
        max_value = max(net_value)
        retracement[i] = (max_value - net_value[i]) / max_value
    result_show.max_retracement = max(retracement)
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
    visible_count = int(len(data) / 5)
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