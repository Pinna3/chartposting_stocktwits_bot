import json
import pandas as pd
from risk_parameter import preset_daily_counter_capacities
from utility_func import pull_top_tier_unbroken_trenders
from candlestick import LiteSecurityTradeData, SecurityTradeData
from momoscreener import LiteSecurities

trender_watchlist_filenames = pull_top_tier_unbroken_trenders(tier_percentage=10)
list_of_almost_consumable_lists = []
for filename in trender_watchlist_filenames:
    if filename is not None:
        with open(filename[0]) as infile:
            watchlist = json.load(infile)
            consumable_list_plus_side = []
            for stock in watchlist:
                ticker = stock['ticker']
                sector = stock['sector']
                peers = stock['peers']
                mktcap = stock['mktcap']
                smoothness = 'TRUE'
                bb_window = stock["bb_window"]
                bb_std = stock['bb_std']
                sma200_double_agent = stock['200sma_double_agent']
                df = pd.read_csv(f"{mktcap}Stocks/Dataframes/{ticker}.csv", index_col=0)
                if 'uptrend' in filename[0]:
                    opt_str = '>'
                elif 'downtrend' in filename[0]:
                    opt_str = '<'
                consumable_list_plus_side.append([opt_str, ticker, mktcap, sector, smoothness, peers, sma200_double_agent, df])
        list_of_almost_consumable_lists.append(consumable_list_plus_side)
candle_object_list_dict = {
    '>': {
        'VeryLarge' : [],
        'Large': [],
        'Medium': [],
        'Small': [],
        'Micro': []
    },
    '<': {
        'VeryLarge' : [],
        'Large': [],
        'Medium': [],
        'Small': [],
        'Micro': []
    }
}
for almost_consumable_list in list_of_almost_consumable_lists:
    for almost_consumable_item in almost_consumable_list:
        candle_object_list_dict[almost_consumable_item[0]][almost_consumable_item[2]].append(LiteSecurityTradeData(almost_consumable_item[1:]))

candles = LiteSecurities(candle_object_list_dict['>']['VeryLarge'])
candles.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
hits = []
for candle in candle_object_list_dict['>']['VeryLarge']:
    candle.sma200_double_agent_activate(candle.sma200_double_agent)
    c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle.df.iloc[-1]
    if l < sma200:
        hits.append(candle)
print(len(hits))
print(len(candle_object_list_dict['>']['VeryLarge']))
# print(trender_watchlist_filenames)
