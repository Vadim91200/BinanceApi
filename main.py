import requests

def get_available_cryptocurrencies():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()

    cryptocurrencies = set()

    for symbol in data['symbols']:
        cryptocurrencies.add(symbol['baseAsset'])
        cryptocurrencies.add(symbol['quoteAsset'])

    return list(cryptocurrencies)

cryptocurrencies = get_available_cryptocurrencies()
print(cryptocurrencies)
def getDepth(direction, pair):
    url = f"https://api.binance.com/api/v3/depth?symbol={pair}&limit=5"
    response = requests.get(url)
    data = response.json()

    if direction.lower() == 'ask':
        # Asks are ordered by price in ascending order, so the first element is the lowest ask price
        price = data['asks'][0][0]
    elif direction.lower() == 'bid':
        # Bids are ordered by price in descending order, so the first element is the highest bid price
        price = data['bids'][0][0]
    else:
        raise ValueError("Direction must be 'ask' or 'bid'")

    return price

ask_price = getDepth('ask', 'BTCUSDT')
bid_price = getDepth('bid', 'BTCUSDT')
print(f"Ask Price: {ask_price}, Bid Price: {bid_price}")
def get_order_book(pair, limit):
    url = f"https://api.binance.com/api/v3/depth?symbol={pair}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    order_book = {
        'bids': data['bids'],
        'asks': data['asks']
    }

    return order_book

order_book = get_order_book('BTCUSDT', 100)
print(order_book)
def refreshDataCandle(pair='BTCUSDT', duration='5m', last_fetched_time=None):
    duration_to_millis = {
        '1m': 60000, '3m': 180000, '5m': 300000, '15m': 900000, '30m': 1800000,
        '1h': 3600000, '2h': 7200000, '4h': 14400000, '6h': 21600000, '8h': 28800000,
        '12h': 43200000, '1d': 86400000, '3d': 259200000, '1w': 604800000, '1M': 2592000000
    }

    # Calculate the start time for the new data request
    if last_fetched_time:
        start_time = last_fetched_time + duration_to_millis.get(duration, 300000)
    else:
        start_time = 0  # If no last fetched time is provided, fetch from the earliest available data

    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={duration}&startTime={start_time}"
    response = requests.get(url)
    data = response.json()

    return data

candle_data = refreshDataCandle('BTCUSDT', '5m')
print(candle_data)
import create_tables from slqTable
create_tables()
import sqlite3

def insert_candle_data(db_name, candle_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO data_candles (date, high, low, open, close, volume)
        VALUES (?, ?, ?, ?, ?, ?)
    '''

    for candle in candle_data:
        cursor.execute(insert_query, candle)

    conn.commit()
    conn.close()

db_name = 'BinanceApi.db'
insert_candle_data(db_name, candle_data)
def refreshData(pair):
    url = f"https://api.binance.com/api/v3/trades?symbol={pair}"
    response = requests.get(url)
    data = response.json()

    return data

# Example usage
trade_data = refreshData('BTCUSDT')
print(trade_data)
import sqlite3

def insert_trade_data(db_name, trade_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    insert_query = '''
        INSERT INTO trade_table (trade_id, price, qty, time, is_buyer_maker)
        VALUES (?, ?, ?, ?, ?)
    '''

    for trade in trade_data:
        trade_tuple = (
            trade['id'], 
            trade['price'], 
            trade['qty'], 
            trade['time'], 
            trade['isBuyerMaker']
        )
        cursor.execute(insert_query, trade_tuple)

    conn.commit()
    conn.close()


db_name = 'BinanceApi.db'
insert_trade_data(db_name, trade_data)
import time

def createOrder(api_key, price, amount, pair, orderType):
    url = "https://api.binance.com/api/v3/order"
    # Define the required payload
    data = {
        'symbol': pair,
        'type': orderType.upper(),
        'timeInForce': 'GTC',  # Good till cancel
        'quantity': amount,
        'timestamp': int(time.time() * 1000)  # Current Unix timestamp
    }

    # Add the API key in the header
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Send POST request to Binance API
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Example usage

response = createOrder("T59MTDLWlpRW16JVeZ2Nju5A5C98WkMm8CSzWC4oqynUlTm1zXOxyauT8LmwXEv9", 'BUY', '50000', '0.001', 'BTCUSD', 'LIMIT')
print(response)
def cancelOrder(api_key, order_id, symbol):
    url = "https://api.binance.com/api/v3/order"

    # Define the required payload
    data = {
        'symbol': symbol,
        'orderId': order_id,
        'timestamp': int(time.time() * 1000)  # Current Unix timestamp
    }

    # Add the API key in the header
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Send DELETE request to Binance API
    response = requests.delete(url, headers=headers, params=data)
    return response.json()

# Example usage

response = cancelOrder("T59MTDLWlpRW16JVeZ2Nju5A5C98WkMm8CSzWC4oqynUlTm1zXOxyauT8LmwXEv9", "215445", 'BTCUSDT')
print(response)
