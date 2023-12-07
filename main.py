from flask import Flask, jsonify, request
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)
cache = {}

def is_market_hours():
    now = datetime.now(pytz.timezone('Asia/Kolkata'))
    return (now.hour >= 9 and now.hour < 15)

def get_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    price = ticker.history(period="1d")['Close'][0]
    return price

def get_cached_stock_price(symbol):
    if symbol in cache:
        return cache[symbol]
    else:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")['Close'][0]
        cache[symbol] = price
        return price

@app.route('/multi-ltp/<symbolList>', methods=['GET'])
def multi_ltp(symbolList):
    symbols = symbolList.split(',')
    ticker = yf.Tickers(' '.join(symbols))
    data = ticker.history(period="1d")['Close']
    return jsonify(data.to_dict())        

@app.route('/ltp/<symbol>', methods=['GET'])
def ltp(symbol):
    if not is_market_hours():
        price = get_stock_price(symbol)
        return jsonify({'symbol': symbol, 'ltp': price, 'timestamp': datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")})
    else:
        price = get_cached_stock_price(symbol)
        return jsonify({'symbol': symbol, 'ltp': price, 'timestamp': datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")})

if __name__ == '__main__':
    app.run(port=3456)
