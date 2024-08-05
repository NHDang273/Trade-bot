import numpy as np
import pandas as pd

class BollingerVWAPInvestment:
    def __init__(self, data, volume, bollinger_window, num_std_dev):

        self.data = data

        self.volume = volume

        self.bollinger_window = bollinger_window

        self.num_std_dev = num_std_dev

    def calculate_vwap(self):
  
        cum_vol = self.volume.cumsum()
        cum_vol_price = (self.volume * self.data).cumsum()
        vwap = cum_vol_price / cum_vol

        return vwap

    def calculate_bollinger_bands(self):
    
        rolling_mean = self.data.rolling(window=self.bollinger_window).mean()
        rolling_std = self.data.rolling(window=self.bollinger_window).std()
        upper_band = rolling_mean + (rolling_std * self.num_std_dev)
        lower_band = rolling_mean - (rolling_std * self.num_std_dev)

        return rolling_mean, upper_band, lower_band

    def BollingerVWAP_signal(self):

        vwap = self.calculate_vwap()

        rolling_mean, upper_band, lower_band = self.calculate_bollinger_bands()

        buy_signal = (self.data < lower_band) & (self.data > vwap)
        sell_signal = (self.data > upper_band) & (self.data < vwap)

        Position = np.where(buy_signal, 1, np.where(sell_signal, -1, 0))

        Signal = np.diff(Position, prepend=Position[0])

        return Signal[-1]
