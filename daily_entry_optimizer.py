import json
import pandas as pd

trender_watchlist_filename = 'MicroStocks/Watchlists/(25,)D-uptrend.json'

#get dataframes for trender  watchlist
with open(trender_watchlist_filename) as infile:
    watchlist = json.load(infile)
    hits = []
    for stock in watchlist:
        ticker = stock['ticker']
        df = pd.read_csv(f"MicroStocks/Dataframes/{ticker}.csv", index_col=0)
        c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = df.iloc[-1]
        #if op_str = '>' (uptrend):
        if sma9 > sma20 and sma20 > sma50 and sma50 > sma200 and c < lower:
            hits.append(ticker)

print(print(hits))
