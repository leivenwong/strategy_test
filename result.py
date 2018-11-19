import strategy_functions as fuc

class Result():
    """define result class"""
    def __init__(self):
        self.net_value = 1
        self.easy_max_retracement = 0
        self.max_retracement = 0
        self.trade_times = 1
        self.stop_times = 0
        self.std = 0
        self.open = 1
        self.close = 1
        self.trade_succeed = 0
        self.max_profit = 0.00001
        self.max_loss = 0.00001
        self.ifstop = 0

    def reset_net_value(self):
        self.net_value = 1

    def update_net_value(self, net_value):
        self.net_value = net_value

    def update_max_pl_up(self):
        if (self.close - self.open) / self.open > self.max_profit:
            self.max_profit = (self.close - self.open) / self.open
        if (self.close - self.open) / self.open < self.max_loss:
            self.max_loss = (self.close - self.open) / self.open

    def update_max_pl_down(self):
        if (self.open - self.close) / self.open > self.max_profit:
            self.max_profit = (self.open - self.close) / self.open
        if (self.open - self.close) / self.open < self.max_loss:
            self.max_loss = (self.open - self.close) / self.open