import functions as fuc

class Result():
    """define result class"""
    def __init__(self):
        self.net_value = 1
        self.max_retracement = 0
        self.trade_times = 0

    def reset_net_value(self):
        self.net_value = 1

    def update_net_value(self, net_value):
        self.net_value = net_value
