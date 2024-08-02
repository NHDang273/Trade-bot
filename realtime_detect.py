import time
import MetaTrader5 as mt5
import pandas as pd
from request import start_mt5, initialize_symbols, place_order, cancel_order, modify_position, get_open_orders, get_open_positions
from indicator_func.RSI import RSIInvestment
import logging
from datetime import datetime


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

def get_realtime_candles(symbol, count):
    # Lấy dữ liệu nến thời gian thực
    candles = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M1, time.time(), count)
    candles_df = pd.DataFrame(candles)

    # Chuyển đổi cột time thành định dạng datetime
    candles_df['time'] = pd.to_datetime(candles_df['time'], unit='s')
    
    # Đổi tên các cột để khớp với yêu cầu
    candles_df.rename(columns={
        'time': 'Datetime',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'tick_volume': 'Volume',
        'spread': 'Dividends',  # Không có thông tin về Dividends trong tick
        'real_volume': 'Stock Splits'  # Không có thông tin về Stock Splits trong tick
    }, inplace=True)

    # Thêm các cột Dividends và Stock Splits mặc định là 0
    candles_df['Dividends'] = 0
    candles_df['Stock Splits'] = 0

    return candles_df

def main():
    # Set up the import filepath
    import_filepath = "E:\WORKSPACE\TradeBot\Trade-bot\dev.json"
    # Import project settings
    project_settings = get_project_settings(import_filepath)

    # Start MT5
    if not start_mt5(project_settings["username"], project_settings["password"], project_settings["server"],
                     project_settings["mt5Pathway"]):
        trade_log("Failed to start MT5", level='error')
        return

    trade_log("MT5 started successfully")

    # Initialize symbols
    initialize_symbols(project_settings["symbols"])

    # Select symbol to run strategy on
    symbol_for_strategy = project_settings['symbols'][0]

    # Create an empty DataFrame to store data
    data = pd.DataFrame(columns=['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'])
    rsi_investment = RSIInvestment(data=data, budget=10000)

    # Get initial data
    data = get_realtime_candles(symbol_for_strategy, 15)  # Lấy 15 nến ban đầu
    if data is not None:
        rsi_investment.data = data.copy()
        rsi_investment.calculate_rsi()
        rsi_investment.generate_signals()
        save_dataframe_to_file(data, 'data_get.txt')

    # Start a while loop to poll MT5
    while True:
        try:
            # Get real-time candles
            new_candles_df = get_realtime_candles(symbol_for_strategy, 1)
            if new_candles_df is not None:
                # Thêm dữ liệu mới vào DataFrame
                data = pd.concat([data, new_candles_df], ignore_index=True)

                # Remove duplicates based on time
                data = data.drop_duplicates(subset=['Datetime'])
                # Giới hạn kích thước của DataFrame để tiết kiệm bộ nhớ
                data = data.tail(1000)  # Giữ lại chỉ 1000 nến gần nhất

                # Save DataFrame to file
                save_dataframe_to_file(data, 'data_get.txt')

                # Calculate RSI and generate signals
                if len(data) > rsi_investment.period:
                    rsi_investment.data = data.copy()
                    rsi_investment.calculate_rsi()
                    rsi_investment.generate_signals()

                    

                    # Print and log the latest signals
                    latest_signal = rsi_investment.data.iloc[-1]
                    message = (f"Time: {latest_signal['Datetime']}, Close: {latest_signal['Close']}, "
                               f"RSI: {latest_signal['RSI']}, Signal: {latest_signal['Signal']}")
                    print(message)
                    trade_log(message)

                    # Execute trades based on signals
                    if latest_signal['Signal'] == 1:
                        trade_log(f"Executing BUY order at {latest_signal['Close']}")
                        # place_order('buy', symbol_for_strategy, latest_signal['Close'])  # Add your order placement logic here
                    elif latest_signal['Signal'] == -1:
                        trade_log(f"Executing SELL order at {latest_signal['Close']}")
                        # place_order('sell', symbol_for_strategy, latest_signal['Close'])  # Add your order placement logic here
                    else:
                        trade_log("No trade signals detected")
                else:
                    print(f"Data length {len(data)} is not greater than RSI period {rsi_investment.period}")

            # Sleep for a short duration before the next update
            time.sleep(60)  # Điều chỉnh thời gian chờ theo nhu cầu
        except Exception as e:
            trade_log(f"Error occurred: {str(e)}", level='error')

if __name__ == "__main__":
    main()
