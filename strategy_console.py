import pandas as pd
import random as rd
import math
import matplotlib.pyplot as plt
import numpy
from numpy.linalg import cholesky
import datetime
import time

from strategy_settings import Settings
import strategy_functions as fuc
import result
import strategy
import sys
sys.path.append('D:\\python_project\\statistics')
from statistics_functions import compute_r

#initiate settings
ai_settings = Settings()
result_show = result.Result()
result_show.reset_net_value()

#read raw data
target_1 = fuc.read_sql_backtesting(ai_settings)
target_1 = pd.DataFrame(target_1)
data = target_1['CLOSE']


print(fuc.compute_rsi(data, 9))