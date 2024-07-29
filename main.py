import MetaTrader5 as mt5
from datetime import datetime

# Chỉ định đường dẫn đến terminal MetaTrader 5
terminal_path = r'C:\Program Files\MetaTrader 5\terminal64.exe'  # Cập nhật đường dẫn này nếu cần

# Khởi tạo MetaTrader 5 với đường dẫn đã chỉ định
if not mt5.initialize(terminal_path):
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Đăng nhập vào tài khoản MetaTrader 5 của bạn
login = 10003860797
password = "!k2cEcPl"
server = 'MetaQuotes-Demo'
if not mt5.login(login, password, server):
    print("login() failed, error code =", mt5.last_error())
    mt5.shutdown()
    quit()

# Lấy thông tin tài khoản
account_info = mt5.account_info()
if account_info is None:
    print("Failed to retrieve account info, error code =", mt5.last_error())
    mt5.shutdown()
    quit()
else:
    print(account_info)

# Hàm ví dụ để đặt lệnh mua
def place_buy_order(symbol, lot, price, slippage, magic, comment):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "slippage": slippage,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order send failed, retcode =", result.retcode)
    else:
        print("Order send successful:", result)

# Hàm ví dụ để lấy dữ liệu biểu tượng
def get_symbol_data(symbol, timeframe, start, end):
    rates = mt5.copy_rates_range(symbol, timeframe, start, end)
    if rates is None:
        print(f"Failed to get symbol data for {symbol}, error code =", mt5.last_error())
    return rates

# Ví dụ sử dụng: đặt lệnh mua
symbol = "EURUSD"
symbol_info = mt5.symbol_info(symbol)

if symbol_info is None:
    print(f"Failed to get symbol info for {symbol}, error code =", mt5.last_error())
else:
    lot = 0.1
    price = symbol_info.ask
    slippage = 10
    magic = 123456
    comment = "Python script order"

    place_buy_order(symbol, lot, price, slippage, magic, comment)

    # Ví dụ sử dụng: lấy dữ liệu biểu tượng
    start = datetime(2022, 1, 1)
    end = datetime.now()
    symbol_data = get_symbol_data(symbol, mt5.TIMEFRAME_D1, start, end)
    if symbol_data is not None:
        print(symbol_data)

# Ngắt kết nối từ MetaTrader 5
mt5.shutdown()
