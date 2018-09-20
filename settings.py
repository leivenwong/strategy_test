class Settings():
    """initiate settings"""
    def __init__(self):
        self.file_path = "399300.xlsx"
        self.sql_path = 'mysql+pymysql://ctp_user:ctp_password@127.0.0.1/ctp_merged_mq?charset=utf8'
        self.fetch_table = 'if_1d'
        self.fetch_date = 'utc_string'
        self.fetch_close = 'close_price'