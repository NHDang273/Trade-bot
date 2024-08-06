from collections import Counter
import numpy as np
import pandas as pd

from indicator_func.SMAInvestment import SMAInvestment
from indicator_func.MACDInvestment import MACDInvestment
from indicator_func.BollingerVWAPInvestment import BollingerVWAPInvestment


class main:
    def __init__(self, data, volume):

        self.signal = []
        self.data = data
        self.volume = volume
    def data(self):
        # return data
        pass

    def volume(self):
        # return data
        pass

    def final_signals(self):

        self.signal.append(SMAInvestment(data = self.data, short_sma = 10, long_sma = 20).Stock_price())

        self.signal.append(MACDInvestment(data = self.data, short_ema = 10, long_ema = 20, signal_ema = 9).MACD_signal())

        self.signal.append(BollingerVWAPInvestment(data = self.data, volume= self.volume, bollinger_window = 20, num_std_dev = 2).BollingerVWAP_signal())
        
    def final_sig(lst):
    
        count = Counter(lst)
            

        max_count = max(count.values())
            
    
        most_common = [k for k, v in count.items() if v == max_count]
            
        
        if len(most_common) > 1:
            return 0
            
        return most_common[0]
    
        # finall = final_sig(self.signal)

        # return finall

    def calculate_profit(self):
        # return profit
        pass
    
    def signal_data(self):
        # return timeseries data from signal
        
        pass
    