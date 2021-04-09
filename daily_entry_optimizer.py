import json
import pandas as pd
from risk_parameter import preset_daily_counter_capacities
from utility_func import pull_top_tier_unbroken_trenders

trender_watchlist_filenames = pull_top_tier_unbroken_trenders(tier_percentage=10)

hits = []
for filename in trender_watchlist_filenames:
    if filename is not None:
        with open(filename[0]) as infile:
            watchlist = json.load(infile)
            for stock in watchlist:
                ticker = stock['ticker']
                mktcap = stock['mktcap']
                df = pd.read_csv(f"{mktcap}Stocks/Dataframes/{ticker}.csv", index_col=0)
                c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = df.iloc[-1]
                #if op_str = '>' (uptrend):
                if sma9 > sma20 and sma20 > sma50 and sma50 > sma200 and l < lower:
                    hits.append(ticker)

print(len(hits))

###Might be easier to just set up the scanner to adjust ror_prioritization_factor based on results of the daily counter. (more robust data that way because
### we're capturing the lows of the day rather than just the close, do high / low instead)
