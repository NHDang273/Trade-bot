import MetaTrader5 as mt5
import pandas as pd
import time
import logging
from collections import Counter
from request import start_mt5, initialize_symbols, place_order, cancel_order, modify_position, get_open_orders, get_open_positions
from indicator_func.RSI import RSIInvestment
from indicator_func.SMAInvestment import SMAInvestment
from indicator_func.BollingerVWAPInvestment import BollingerVWAPInvestment
from indicator_func.MACDInvestment import MACDInvestment


# Set up logging to log into a text file
logging.basicConfig(filename='trade_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_project_settings(filepath):
    import json
    with open(filepath, 'r') as f:
        return json.load(f)

def trade_log(message, level='info'):
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)

def save_dataframe_to_file(df, filename):
    try:
        df.to_csv(filename, mode='a', index=False, header=False)
        trade_log(f"DataFrame saved to {filename}")
    except Exception as e:
        trade_log(f"Failed to save DataFrame to {filename}: {str(e)}", level='error')

def get_realtime_data(symbol, count):
    candles = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, time.time(), count)
    candles_df = pd.DataFrame(candles)
    candles_df['time'] = pd.to_datetime(candles_df['time'], unit='s')
    candles_df.rename(columns={
        'time': 'Datetime', 'open': 'Open', 'high': 'High',
        'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume',
        'spread': 'Dividends', 'real_volume': 'Stock Splits'
    }, inplace=True)
    candles_df['Dividends'] = 0
    candles_df['Stock Splits'] = 0
    return candles_df

def final_signals(rsi, macd, bband, sma):
    signal = [rsi, macd, bband, sma]
    count = Counter(signal)
    max_count = max(count.values())
    most_common = [k for k, v in count.items() if v == max_count]
    if len(most_common) > 1:
        return 0
    return most_common[0]


def execute_trade(signal, symbol):
    if signal == 1:
        place_order(order_type="BUY",symbol=symbol, volume=0.1)
    elif signal == -1:
        place_order(order_type="SELL",symbol=symbol, volume=0.1)
    else:
        trade_log("No signal to execute")

def calculate_indicators(data, budget):
    try:
        rsi_investment = RSIInvestment(data=data.copy(), budget=budget)
        rsi_investment.calculate_rsi()
        signals_rsi = rsi_investment.generate_signals()
        latest_rsi = rsi_investment.data['RSI'].iloc[-1]
        print(f"RSI signals generated: {signals_rsi}")
        trade_log(f"RSI signals generated: {signals_rsi}")
    except Exception as e:
        trade_log(f"Failed to generate RSI signals: {str(e)}", level='error')
        signals_rsi = 0

    try:
        macd_investment = MACDInvestment(data=data['Close'], short_ema=10, long_ema=20, signal_ema=9)
        signals_macd = macd_investment.MACD_signal()
        print(f"MACD signals generated: {signals_macd}")
        trade_log(f"MACD signals generated: {signals_macd}")
    except Exception as e:
        trade_log(f"Failed to generate MACD signals: {str(e)}", level='error')
        signals_macd = 0

    try:
        bband_investment = BollingerVWAPInvestment(data=data['Close'], volume=data['Volume'], bollinger_window=20, num_std_dev=2)
        bband_investment.calculate_bollinger_bands()
        bband_investment.calculate_vwap()
        signals_bband = bband_investment.BollingerVWAP_signal()
        print(f"Bollinger Band signals generated: {signals_bband}")
        trade_log(f"Bollinger Band signals generated: {signals_bband}")
    except Exception as e:
        trade_log(f"Failed to generate Bollinger Band signals: {str(e)}", level='error')
        signals_bband = 0

    try:
        sma_investment = SMAInvestment(data=data['Close'], short_sma=10, long_sma=20)
        signals_sma = sma_investment.Stock_price()
        print(f"SMA signals generated: {signals_sma}")
        trade_log(f"SMA signals generated: {signals_sma}")
    except Exception as e:
        trade_log(f"Failed to generate SMA signals: {str(e)}", level='error')
        signals_sma = 0

    return signals_rsi, signals_macd, signals_bband, signals_sma

def main():
    import_filepath = "E:/WORKSPACE/TradeBot/Trade-bot/dev.json"
    project_settings = get_project_settings(import_filepath)

    if not start_mt5(project_settings["username"], project_settings["password"], project_settings["server"],
                     project_settings["mt5Pathway"]):
        print("Failed to start MT5")
        return

    trade_log("MT5 started successfully")
    initialize_symbols(project_settings["symbols"])
    symbol_for_strategy = project_settings['symbols'][0]
    data = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])

    try:
        data = get_realtime_data(symbol_for_strategy, 15)
        print("Real-time data retrieved")
        # print(data)
    except Exception as e:
        trade_log(f"Failed to get real-time data: {str(e)}", level='error')
        return

    while True:
        try:
            new_candles_df = get_realtime_data(symbol_for_strategy, 1)
            if new_candles_df is not None:
                data = pd.concat([data, new_candles_df], ignore_index=True)
                data = data.drop_duplicates(subset=['Datetime'])

                print(data)

                signals_rsi, signals_macd, signals_bband, signals_sma = calculate_indicators(data, project_settings["budget"])
                final_signal = final_signals(signals_rsi, signals_macd, signals_bband, signals_sma)
                print(f"Final signal: {final_signal}")
                trade_log(f"Final signal: {final_signal}")

                execute_trade(final_signal, symbol_for_strategy)

            else:
                print("No new data retrieved")

            time.sleep(60)
        except Exception as e:
            trade_log(f"An error occurred: {str(e)}", level='error')
            print(f"An error occurred: {str(e)}")
            break

if __name__ == "__main__":
    main()
