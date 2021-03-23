from candlestick import DailyCandleDataRT
import finnhub
import json
import operator
from time import sleep

def dailyscanner(json_watchlist, op_str):
    with open(json_watchlist) as infile:
        watchlist = json.load(infile)

    # Setup finnhub client connection
    finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
    #up/down trendtrend toggle
    ops = {"<": operator.lt, ">": operator.gt}
    op_func = ops[op_str]
    opposite_ops = {">": operator.lt, "<": operator.gt}
    opposite_op_func = opposite_ops[op_str]
    #loop through securities and filter for up/down trends
    hits = []
    for index, security in enumerate(watchlist):
        sleep(1)
        try:
            # print(security)
            candle_object = DailyCandleDataRT(security['ticker'], 365, security['bb_window'], security['bb_std'])
            c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-1]
            if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                opposite_op_func(c, lower): ####make interchangeable for shorts
                hits.append({'ticker': security['ticker'], 'industry': security['industry']})
                # candle_object.chart(120)
                # print(hits)
            else:
                print(index)
        except:
            continue

    sectors = {}
    for security in hits:
        if security['industry'] not in sectors.keys():
            sectors[security['industry']] = 1
        else:
            sectors[security['industry']] += 1
    print(sectors)


dailyscanner('ticker_dict.json', '>')
