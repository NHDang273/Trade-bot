import MetaTrader5 as mt5
from datetime import datetime
import pytz
import pandas as pd

def initialize_mt5():
    """Khởi tạo kết nối với MetaTrader 5."""
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())
        return False
    return True

def login_mt5(login, password, server):
    """Đăng nhập vào tài khoản MetaTrader 5."""
    if not mt5.login(login, password, server):
        print("login() failed, error code =", mt5.last_error())
        return False
    return True

def get_xauusd_data(start_date, end_date, timeframe=mt5.TIMEFRAME_M5):
    """Lấy dữ liệu lịch sử từ cặp XAU/USD."""
    symbol = "XAUUSD"

    # Kiểm tra xem cặp có sẵn không
    if not mt5.symbol_select(symbol, True):
        print(f"Failed to select {symbol}, error code =", mt5.last_error())
        return None

    # Lấy dữ liệu lịch sử
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

    # Kiểm tra nếu có dữ liệu
    if rates is None:
        print("Failed to get data, error code =", mt5.last_error())
        return None

    return rates

def print_account_info():
    """In thông tin tài khoản."""
    account_info = mt5.account_info()
    
    if account_info is None:
        print("Failed to retrieve account info, error code =", mt5.last_error())
    else:
        print("Account Information:")
        print(f"Account Number: {account_info.login}")
        print(f"Balance: {account_info.balance}")
        print(f"Equity: {account_info.equity}")
        print(f"Margin: {account_info.margin}")
        print(f"Free Margin: {account_info.margin_free}")
        print(f"Leverage: {account_info.leverage}")
        print(f"Account Type: {account_info.trade_mode}")

def display_rates(rates):
    """Hiển thị dữ liệu lịch sử."""
    # Tạo DataFrame từ dữ liệu lịch sử
    df = pd.DataFrame(rates)
    
    # Đổi tên cột
    df.columns = ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
    
    # In 5 dòng đầu tiên
    print(df.head())

def order_history(start_date, end_date):
    """Lấy lịch sử giao dịch."""
    # Lấy lịch sử giao dịch
    orders = mt5.history_orders_get(start_date, end_date)
    
    # Kiểm tra nếu có lịch sử giao dịch
    if orders is None:
        print("Failed to get order history, error code =", mt5.last_error())
        return

    # Danh sách để lưu dữ liệu lịch sử giao dịch
    order_data = []

    # Lưu thông tin từng giao dịch vào danh sách
    for order in orders:
        order_info = {
            'Order ID': order.ticket,
            'Symbol': order.symbol,
            'Volume': order.volume,
            'Type': 'Buy' if order.type == mt5.ORDER_BUY else 'Sell',
            'Price': order.price_open,
            'Profit': order.profit,
            'Open Time': datetime.fromtimestamp(order.time),
            'Close Time': datetime.fromtimestamp(order.time_done),
        }
        order_data.append(order_info)

    # Chuyển đổi danh sách thành DataFrame để hiển thị
    df = pd.DataFrame(order_data)
    
    # In ra DataFrame
    print("Order History:")
    print(df)

# Sử dụng các hàm
if __name__ == "__main__":
    # Thay đổi thông tin đăng nhập và thời gian theo nhu cầu
    login = 10003860797
    password = "!k2cEcPl"
    server = 'MetaQuotes-Demo'
    
    # Thiết lập múi giờ UTC
    timezone = pytz.timezone("Etc/UTC")
    
    # Tạo các đối tượng datetime ở múi giờ UTC
    start = datetime(2024, 7, 1, tzinfo=timezone)  
    end = datetime(2024, 7, 29, tzinfo=timezone)  

    # Khởi tạo MetaTrader 5
    if initialize_mt5():
        # Đăng nhập vào MetaTrader 5
        if login_mt5(login, password, server):
            # In thông tin tài khoản
            print_account_info()

            # Lấy dữ liệu XAU/USD
            xauusd_data = get_xauusd_data(start, end)
            
            if xauusd_data is not None:
                for rate in xauusd_data:
                    print(rate)

            # hiển thị oder history
            order_history(start, end)
            

        # Ngắt kết nối với MetaTrader 5
        mt5.shutdown()
