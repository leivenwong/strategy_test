import pandas as pd
from sqlalchemy import create_engine
import pymysql


#read data setting
data_read_user_1 = 'wang_2'
data_read_psd_1 = 'wang_2'
data_read_db_1 = 'python_merge'

data_read_user_2 = 'wang_2'
data_read_psd_2 = 'wang_2'
data_read_db_2 = 'wang_2'

#write data setting
data_write_user = 'ctp_user'
data_write_psd = 'ctp_password'
data_write_db = 'ctp_merged_mq'

#merge table list
table_level_list = ['5s']
#table_level_list = ['1m', '5m', '15m', '1h', '1d']
#table_name_list = ['ih', 'ic', 'ru', 'rb']
table_name_list = ['if', 'ih', 'ic', 'ru', 'rb']


#data merge cycle
for name in table_name_list:
    for level in table_level_list:
        table_name = name + '_' + level
        print("Enter Mysql wang1 " + table_name)
        engine = create_engine('mysql+pymysql://'
                               + data_read_user_1 + ':'
                               + data_read_psd_1 +
                               '@127.0.0.1/' +
                               data_read_db_1 +
                               '?charset=utf8')
        df = pd.read_sql(sql="select * from " + table_name, con=engine)
        print("Out Mysql wang1 " + table_name)
        wang1 = df
        wang1 = pd.DataFrame(wang1)

        print("Enter Mysql wang2 " + table_name)
        engine = create_engine('mysql+pymysql://'
                               + data_read_user_2 + ':'
                               + data_read_psd_2 +
                               '@127.0.0.1/' +
                               data_read_db_2 +
                               '?charset=utf8')
        df = pd.read_sql(sql="select * from " + table_name, con=engine)
        print("Out Mysql wang2 " + table_name)
        wang2 = df
        wang2 = pd.DataFrame(wang2)
        #type_name = [name] * len(wang2['type'])
        #wang2['type'] = type_name

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
        connect = pymysql.connect(
            user=data_write_user,
            password=data_write_psd,
            host="127.0.0.1",
            port=3306,
            db=data_write_db,
            charset="utf8"
        )
        conn = connect.cursor()  # 创建操作游标
        conn.execute("drop table if exists " + table_name)  # 如果表存在则删除
        sql = "create table " + table_name + \
              "(utc BIGINT(20), " \
              "utc_string CHAR(50), " \
              "type CHAR(50), " \
              "open_price DOUBLE, " \
              "high_price DOUBLE, " \
              "low_price DOUBLE, " \
              "close_price DOUBLE, " \
              "volumn BIGINT(20), " \
              "counter INT(11), " \
              "PRIMARY KEY (`utc`))"
        conn.execute(sql)  # 创建表

        engine = create_engine('mysql+pymysql://'
                               + data_write_user + ':'
                               + data_write_psd +
                               '@127.0.0.1/' +
                               data_write_db +
                               '?charset=utf8')
        out.to_sql(table_name, engine, if_exists='append', index=False)

        conn.close()  # 关闭游标连接
        connect.close()  # 关闭数据库服务器连接 释放内存
        print('write completed')
