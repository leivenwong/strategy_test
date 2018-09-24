class Settings():
    """initiate settings"""
    def __init__(self):
        #read excel file' path
        self.file_path = "399300.xlsx"

        #read Mysql database's path
        self.sql_path = 'mysql+pymysql://ctp_user:ctp_password' \
            '@127.0.0.1/ctp_merged_mq?charset=utf8'

        #set which table will used in mysql database
        self.fetch_table = 'if_1d'

        #fetch date column in raw data
        self.fetch_date = 'utc_string'

        #fetch close price in raw data
        self.fetch_close = 'close_price'

        #set trade fee
        self.trade_fee = 0.0000325

        #if only buy
        self.only_buy = False

        #if want to draw polt
        self.draw_plot = False