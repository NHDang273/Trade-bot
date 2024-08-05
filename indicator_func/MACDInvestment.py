import numpy as np
import pandas as pd

class MACDInvestment:
    def __init__(self, data, short_ema, long_ema, signal_ema):

        self.data = data

        self.short_ema = short_ema

        self.long_ema = long_ema
        
        self.signal_ema = signal_ema

    def MACD_signal(self):
     
        Short_EMA = self.data.ewm(span=self.short_ema, adjust=False).mean()
        Long_EMA = self.data.ewm(span=self.long_ema, adjust=False).mean()

        MACD = Short_EMA - Long_EMA

        Signal_Line = MACD.ewm(span=self.signal_ema, adjust=False).mean()

        buy_signal = (MACD < 0) & (Signal_Line < 0) & (MACD > Signal_Line)
        sell_signal = (MACD > 0) & (Signal_Line > 0) & (MACD < Signal_Line)

        Position = np.where(buy_signal, 1, np.where(sell_signal, -1, 0)) 

        Signal = np.diff(Position, prepend=Position[0])

        return Signal[-1]