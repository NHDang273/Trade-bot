import numpy as np

class MACDInvestment:
    def __init__(self, data, budget, short_window=12, long_window=26, signal_window=9):
        self.data = data
        self.budget = budget
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window
        self.data['Signal'] = 0

    def calculate_macd(self):
        self.data['ShortEMA'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.data['LongEMA'] = self.data['Close'].ewm(span=self.long_window, adjust=False).mean()
        self.data['MACD'] = self.data['ShortEMA'] - self.data['LongEMA']
        self.data['SignalLine'] = self.data['MACD'].ewm(span=self.signal_window, adjust=False).mean()

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.signal_window:, 'Signal'] = np.where(
            self.data['MACD'][self.signal_window:] > self.data['SignalLine'][self.signal_window:], 1, 0
        )
        return self.data[['Signal']]

    def print_trade_signals(self):
        print(self.data[['Datetime', 'Signal']])
