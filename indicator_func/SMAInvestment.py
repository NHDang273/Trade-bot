import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  
from datetime import datetime

class SMAInvestment:
    def __init__(self, data, short_sma, long_sma):

        self.data      = data

        self.short_sma = short_sma
        
        self.long_sma  = long_sma


    def Stock_price(self):

        Short_SMA       = self.data.rolling(window = self.short_sma, min_periods = 1).mean()
        Long_SMA        = self.data.rolling(window = self.long_sma, min_periods = 1).mean()

        Position        = np.where(Short_SMA > Long_SMA, 1, 0)
        Position_array  = np.array(Position)

        Signal          = np.diff(Position_array, prepend = Position_array[0])

        return Signal[-1]
