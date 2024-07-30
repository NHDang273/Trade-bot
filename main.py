from Method import start_mt5, initialize_symbols, query_historic_data, place_order, get_open_orders, get_open_positions
import MetaTrader5 as mt5  

def main():
    username = "10003860797"
    password = "!k2cEcPl"
    server = "MetaQuotes-Demo"
    path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # Cập nhật đường dẫn đúng với nơi bạn đã cài đặt MT5

    # Khởi động MetaTrader 5
    if start_mt5(username, password, server, path):
        symbols = ["XAUUSD"]
        
        # Khởi tạo các cặp tiền tệ
        if initialize_symbols(symbols):
            historic_data = query_historic_data("XAUUSD", "M1", 10)
            print("Historic Data for XAUUSD:", historic_data)

            # Lấy thông tin về cặp tiền tệ
            symbol_info = mt5.symbol_info("XAUUSD")
            if symbol_info is None:
                print("Could not retrieve symbol information.")
                mt5.shutdown()
                return

            point = symbol_info.point

            # Lấy giá Ask hiện tại
            tick_info = mt5.symbol_info_tick("XAUUSD")
            if tick_info is None:
                print("Could not retrieve tick information.")
                mt5.shutdown()
                return

            current_price = tick_info.ask

            # Cập nhật giá trị SL và TP
            stop_loss = current_price - 5   # SL 20 pips dưới giá Ask
            take_profit = current_price + 5  # TP 20 pips trên giá Ask

            # Đảm bảo SL và TP hợp lệ
            if stop_loss < current_price and take_profit > current_price:
                # Đặt lệnh mua
                order_result = place_order("BUY", "XAUUSD", volume=0.01, price=current_price, stop_loss=stop_loss, take_profit=take_profit, comment="Test Order")
                
                if order_result is not None:
                    print("Order Result:", order_result)
                else:
                    print("Lỗi vãi L.")
            else:
                print("Invalid Stop Loss or Take Profit values.")

            # Lấy các lệnh mở
            open_orders = get_open_orders()
            print("Open Orders:", open_orders)
            
            # Lấy các vị thế mở
            open_positions = get_open_positions()
            print("Open Positions:", open_positions)

        # Tắt MT5
        mt5.shutdown()

if __name__ == "__main__":
    main()
