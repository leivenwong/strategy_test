class Settings():
    """initiate settings"""
    def __init__(self):
        #read excel file' path
        self.file_path = "macro.xlsx"

        #read Mysql database's path
        self.sql_path_merged = 'mysql+pymysql://ctp_user:ctp_password' \
            '@127.0.0.1/ctp_merged_mq?charset=utf8'
        self.sql_path_backtesting = 'mysql+pymysql://ctp_user:ctp_password' \
            '@127.0.0.1/ctp_backtesting?charset=utf8'

        #set which table will used in mysql database
        self.fetch_table = 'if_1d'

        #fetch date column in raw data
        self.fetch_close = "close_price"

        #fetch open
        self.fetch_open = "open_price"

        #fetch high
        self.fetch_high = "high_price"

        #fetch low
        self.fetch_low = "low_price"

        #fetch close price in raw data
        self.fetch_date = "utc_string"

        #set trade fee
        self.trade_fee = 0.0000325

        #set leverage
        self.leverage_rate = 1

        #if stop
        self.stop = 0.08

        #if stopwin
        self.stopwin = 1

        #if only buy
        self.only_buy = False

        #if want to draw polt
        self.draw_plot = True

