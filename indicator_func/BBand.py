import numpy as np

class BollingerBandInvestment:
    def __init__(self, data, budget, window=20, num_std_dev=2):
        self.data = data
        self.budget = budget
        self.window = window
        self.num_std_dev = num_std_dev
        self.data['Signal'] = 0

    def calculate_bollinger_bands(self):
        self.data['MiddleBand'] = self.data['Close'].rolling(window=self.window).mean()
        self.data['StdDev'] = self.data['Close'].rolling(window=self.window).std()
        self.data['UpperBand'] = self.data['MiddleBand'] + (self.data['StdDev'] * self.num_std_dev)
        self.data['LowerBand'] = self.data['MiddleBand'] - (self.data['StdDev'] * self.num_std_dev)

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.window:, 'Signal'] = np.where(
            self.data['Close'][self.window:] > self.data['UpperBand'][self.window:], -1, 
            np.where(self.data['Close'][self.window:] < self.data['LowerBand'][self.window:], 1, 0)
        )
        return self.data[['Signal']]

    def print_trade_signals(self):
        print(self.data[['Datetime', 'Signal']])
