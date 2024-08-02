import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class RSIInvestment:
    def __init__(self, data, budget, period=14):
        self.data = data
        self.budget = budget
        self.period = period
        self.signals = None
        self.profit = 0

    def calculate_rsi(self):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=self.period, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        self.data['RSI'] = rsi

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.data['RSI'] < 30, 'Signal'] = 1
        self.data.loc[self.data['RSI'] > 70, 'Signal'] = -1

    def calculate_profit(self):
        position = 0
        self.profit = 0
        for i in range(len(self.data)):
            if self.data['Signal'][i] == 1 and position == 0:
                position = self.budget // self.data['Close'][i]
                self.budget -= position * self.data['Close'][i]
            elif self.data['Signal'][i] == -1 and position > 0:
                self.budget += position * self.data['Close'][i]
                self.profit += (self.data['Close'][i] - self.data['Close'][i-1]) * position
                position = 0

        change_rate = (self.profit / (self.budget + self.profit)) * 100
        return self.profit, change_rate

    def plot_data(self):
        plt.figure(figsize=(12,8))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.data['RSI'], label='RSI')
        plt.axhline(30, linestyle='--', alpha=0.5, color='r')
        plt.axhline(70, linestyle='--', alpha=0.5, color='r')
        plt.scatter(self.data.index, self.data['Signal'], label='Signals', color='black')
        plt.legend()
        plt.show()

    def print_trade_signals(self):
        buy_signals = self.data[self.data['Signal'] == 1]
        sell_signals = self.data[self.data['Signal'] == -1]

        print("Buy Signals:")
        for date, row in buy_signals.iterrows():
            print(f"Date: {date}, Price: {row['Close']}")

        print("\nSell Signals:")
        for date, row in sell_signals.iterrows():
            print(f"Date: {date}, Price: {row['Close']}")