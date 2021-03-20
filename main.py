from candlestick import DailyCandleDataRT
import json
from time import sleep

with open('strong-uptrend03-19-21.json') as infile:
    strong_upstocks = json.load(infile)

for stock in strong_upstocks:
    try:
        sleep(1)
        candlestick_data = DailyCandleDataRT(stock, 365, 20, 2)
        current_price = candlestick_data.df.iloc[-1]
        if current_price['c'] < current_price['lower'] and current_price['sma9'] > current_price['sma20'] > current_price['sma50'] > current_price['sma200']:
            print(f'{candlestick_data.ticker}: BUY BUY BUY BUY BUY BUY BUY!!!')
            candlestick_data.chart(120)
        else:
            print(f'{candlestick_data.ticker} out of range.')
    except:
        continue
