import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import cholesky
import datetime
import time
from sqlalchemy import create_engine

import strategy_functions as fuc
import sys

table_level_list = ['_1m', '_5m', '_15m', '_1h', '_1d']
table_name_list = ['if', 'ih', 'ic', 'ru', 'rb']

for name in table_name_list:
    for level in table_level_list:
        table_name = name + level
        print("Enter Mysql wang1 " + table_name)
        engine = create_engine('mysql+pymysql://ctp_user:ctp_password'
                               '@127.0.0.1/ctp_merged_mq?charset=utf8')
        df = pd.read_sql(sql="select * from " + table_name, con=engine)
        print("Out Mysql wang1 " + table_name)
        wang1 = df
        wang1 = pd.DataFrame(wang1)

        print("Enter Mysql wang2 " + table_name)
        engine = create_engine('mysql+pymysql://wang_2:wang_2'
                               '@127.0.0.1/wang_2?charset=utf8')
        df = pd.read_sql(sql="select * from " + table_name, con=engine)
        print("Out Mysql wang2 " + table_name)
        wang2 = df
        wang2 = pd.DataFrame(wang2)

        merged_data = pd.merge(wang1, wang2, on='utc', how='outer')

        cub = len(merged_data)
        utc = []
        utc_string = []
        type = []
        open_price = []
        high_price = []
        low_price = []
        close_price = []
        volumn = []
        counter = []

        print("merge begin...")
        for i in range(cub):
            # utc
            utc.append(merged_data.loc[i, 'utc'])

            # utc_string
            if pd.isnull(merged_data.loc[i, 'utc_string_x']):
                utc_string.append(merged_data.loc[i, 'utc_string_y'])
            elif pd.isnull(merged_data.loc[i, 'utc_string_y']):
                utc_string.append(merged_data.loc[i, 'utc_string_x'])
            else:
                utc_string.append(merged_data.loc[i, 'utc_string_x'])

            # type
            if pd.isnull(merged_data.loc[i, 'type_x']):
                type.append(merged_data.loc[i, 'type_y'])
            elif pd.isnull(merged_data.loc[i, 'type_y']):
                type.append(merged_data.loc[i, 'type_x'])
            else:
                type.append(merged_data.loc[i, 'type_x'])

            # open_price
            if pd.isnull(merged_data.loc[i, 'open_price_x']):
                open_price.append(merged_data.loc[i, 'open_price_y'])
            elif pd.isnull(merged_data.loc[i, 'open_price_y']):
                open_price.append(merged_data.loc[i, 'open_price_x'])
            else:
                open_price.append(merged_data.loc[i, 'open_price_x'])

            # high_price
            if pd.isnull(merged_data.loc[i, 'high_price_x']):
                high_price.append(merged_data.loc[i, 'high_price_y'])
            elif pd.isnull(merged_data.loc[i, 'high_price_y']):
                high_price.append(merged_data.loc[i, 'high_price_x'])
            elif merged_data.loc[i, 'high_price_x'] > \
                    merged_data.loc[i, 'high_price_y']:
                high_price.append(merged_data.loc[i, 'high_price_x'])
            elif merged_data.loc[i, 'high_price_y'] > \
                    merged_data.loc[i, 'high_price_x']:
                high_price.append(merged_data.loc[i, 'high_price_y'])
            else:
                high_price.append(merged_data.loc[i, 'high_price_x'])

            # low
            if pd.isnull(merged_data.loc[i, 'low_price_x']):
                low_price.append(merged_data.loc[i, 'low_price_y'])
            elif pd.isnull(merged_data.loc[i, 'low_price_y']):
                low_price.append(merged_data.loc[i, 'low_price_x'])
            elif merged_data.loc[i, 'low_price_x'] < \
                    merged_data.loc[i, 'low_price_y']:
                low_price.append(merged_data.loc[i, 'low_price_x'])
            elif merged_data.loc[i, 'low_price_y'] < \
                    merged_data.loc[i, 'low_price_x']:
                low_price.append(merged_data.loc[i, 'low_price_y'])
            else:
                low_price.append(merged_data.loc[i, 'low_price_x'])

            # close
            if pd.isnull(merged_data.loc[i, 'close_price_x']):
                close_price.append(merged_data.loc[i, 'close_price_y'])
            elif pd.isnull(merged_data.loc[i, 'close_price_y']):
                close_price.append(merged_data.loc[i, 'close_price_x'])
            elif merged_data.loc[i, 'counter_x'] > \
                    merged_data.loc[i, 'counter_y']:
                close_price.append(merged_data.loc[i, 'close_price_x'])
            elif merged_data.loc[i, 'counter_y'] > \
                    merged_data.loc[i, 'counter_x']:
                close_price.append(merged_data.loc[i, 'close_price_y'])
            else:
                close_price.append(merged_data.loc[i, 'close_price_x'])

            # volumn
            if pd.isnull(merged_data.loc[i, 'volumn_x']):
                volumn.append(merged_data.loc[i, 'volumn_y'])
            elif pd.isnull(merged_data.loc[i, 'volumn_y']):
                volumn.append(merged_data.loc[i, 'volumn_x'])
            elif merged_data.loc[i, 'counter_x'] > \
                    merged_data.loc[i, 'counter_y']:
                volumn.append(merged_data.loc[i, 'volumn_x'])
            elif merged_data.loc[i, 'counter_y'] > \
                    merged_data.loc[i, 'counter_x']:
                volumn.append(merged_data.loc[i, 'volumn_y'])
            else:
                volumn.append(merged_data.loc[i, 'volumn_x'])

            # counter
            if pd.isnull(merged_data.loc[i, 'counter_x']):
                counter.append(merged_data.loc[i, 'counter_y'])
            elif pd.isnull(merged_data.loc[i, 'counter_y']):
                counter.append(merged_data.loc[i, 'counter_x'])
            elif merged_data.loc[i, 'counter_x'] > \
                    merged_data.loc[i, 'counter_y']:
                counter.append(merged_data.loc[i, 'counter_x'])
            elif merged_data.loc[i, 'counter_y'] > \
                    merged_data.loc[i, 'counter_x']:
                counter.append(merged_data.loc[i, 'counter_y'])
            else:
                counter.append(merged_data.loc[i, 'counter_x'])

        print("merged complete")
        out = []
        out = pd.DataFrame(out)
        out['utc'] = utc
        out['utc_string'] = utc_string
        out['type'] = type
        out['open_price'] = open_price
        out['high_price'] = high_price
        out['low_price'] = low_price
        out['close_price'] = close_price
        out['volumn'] = volumn
        out['counter'] = counter
        print('write mysql')
        engine = create_engine(
            'mysql+pymysql://wang_2:wang_2@127.0.0.1/python_merge?charset=utf8')
        out.to_sql(table_name, engine, if_exists='replace', index=False)
        print('write completed')
