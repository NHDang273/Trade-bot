import time
import MetaTrader5 as mt5
from request import start_mt5, initialize_symbols, query_historic_data, place_order, get_open_orders, get_open_positions, cancel_order, modify_position
import strategy

def get_project_settings(filepath):
    import json
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    # Set up the import filepath
    import_filepath = "E:\WORKSPACE\TradeBot\Trade-bot\dev.json"
    # Import project settings
    project_settings = get_project_settings(import_filepath)

    # Start MT5
    if start_mt5(project_settings["username"], project_settings["password"], project_settings["server"],
                 project_settings["mt5Pathway"]):
        # Initialize symbols
        initialize_symbols(project_settings["symbols"])

        # Select symbol to run strategy on
        symbol_for_strategy = project_settings['symbols'][0]

        # Set up a previous time variable
        previous_time = 0

        # Start a while loop to poll MT5
        while True:
            # Retrieve the current candle data
            candle_data = query_historic_data(symbol=symbol_for_strategy,
                                              timeframe=project_settings['timeframe'], number_of_candles=1)
            # Extract the time data
            current_time = candle_data[0][0]

            # Compare against previous time
            if current_time != previous_time:
                # Notify user
                print("New Candle")
                # Update previous time
                previous_time = current_time
                # Retrieve previous orders
                orders = get_open_orders()
                # Cancel orders
                for order in orders:
                    cancel_order(order)
                # Start strategy one on selected symbol
                strategy.strategy_one(symbol=symbol_for_strategy, timeframe=project_settings['timeframe'],
                                      pip_size=project_settings['pip_size'])
            else:
                # Get positions
                positions = get_open_positions()
                # Pass positions to update_trailing_stop
                for position in positions:
                    strategy.update_trailing_stop(order=position, trailing_stop_pips=10,
                                                  pip_size=project_settings['pip_size'])
            time.sleep(0.1)

if __name__ == "__main__":
    main()
