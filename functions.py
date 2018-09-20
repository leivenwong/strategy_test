import pandas as pd
import random as rd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from settings import Settings

def read_sql(ai_settings):
    engine = create_engine(ai_settings.sql_path)
    df = pd.read_sql(sql="select * from "+ai_settings.fetch_table, con=engine)
    return df

def read_file(ai_settings):
    """read data from data_path"""
    ai_settings = Settings()
    file_path = ai_settings.file_path
    loads = pd.read_excel(file_path)
    return loads

def compute_ma(data,cycle):
    ma_cycle = list(range(len(data)))
    for i in range(cycle):
        ma_cycle[i] = data[0]
    for i in range(cycle, len(data)):
        ma_cycle[i] = (sum(data[i - cycle:i])) / cycle
    return ma_cycle

def compute_net_value(data, direction):
    net_value = list(range(len(data)))
    net_value[0] = 1
    for i in range(1, len(data)):
        if direction[i - 1] == 1:
            net_value[i] = net_value[i - 1] * ((data[i] - data[i - 1]) / data[i - 1] + 1)
        elif direction[i - 1] == -1:
            net_value[i] = net_value[i - 1] * ((data[i - 1] - data[i]) / data[i - 1] + 1)
        else:
            net_value[i] = net_value[i - 1]
        print(net_value[i])
    return net_value

def frofit_per(data_close):
    """compute profit rate per day or other cycle"""
    profit_per = list(range(len(data_close)))
    profit_per[0] = 0
    for i in range(1, len(data_close)):
        profit_per[i] = (data_close[i] / data_close[i - 1] - 1) * 100
    return profit_per

def set_xlable_visible(data):
    ax = plt.gca()
    visible_count = int(len(data) / 5)
    for ind, label in enumerate(ax.xaxis.get_ticklabels()):
        if ind % visible_count == 0:  # set visible number of x lable
            label.set_visible(True)
        else:
            label.set_visible(False)
    ax = plt.gca()
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(0)

def date_left(data):
    for i in range(len(data)):
       data[i] = data[i][0:10]
    return  data