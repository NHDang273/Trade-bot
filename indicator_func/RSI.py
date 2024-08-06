import numpy as np

class RSIInvestment:
    def __init__(self, data, budget, period=14):
        self.data = data
        self.budget = budget
        self.period = period
        self.data['RSI'] = 0
        self.data['Signal'] = 0

    def calculate_rsi(self):
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] < 30, 'Signal'] = 1
        self.data.loc[self.data['RSI'] > 70, 'Signal'] = -1
        # return self.data[['Signal']]
        return self.data.iloc[-1]['Signal']

    def print_trade_signals(self):
        print(self.data[['Datetime', 'Signal']])
