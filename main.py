class main:
    def __init__(self):
        pass
    def data(self):
        # return data
        pass
    def rsi_investment(self, data, budget, period=14):
        self.data = data
        self.budget = budget
        self.period = period
        self.signals = None
        self.profit = 0
        # return [ -1, 0, 1]
    def macd_investment(self, data, budget, period=14):
        self.data = data
        self.budget = budget
        self.period = period
        self.signals = None
        self.profit = 0
        # return [ -1, 0, 1]
    def final_signals(self):
        # return final_signals
        pass
    def calculate_profit(self):
        # return profit
        pass
    def signal_data(self):
        # return timeseries data from signal
        
        pass
    