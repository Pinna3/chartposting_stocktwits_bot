from candlestick import SecurityTradeData
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
            print(security['ticker'])
            candle_object = SecurityTradeData(security['ticker'], 365)
            candle_object.custom_bollingers(security['bb_window'], security['bb_std'])
            c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-1]
            if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                opposite_op_func(c, lower): ####make interchangeable for shorts
                hits.append({'ticker': security['ticker'], 'industry': security['industry']})
                print('Hit! Hit! Hit! Hit! Hit! Hit! Hit! Hit! Hit! Hit! Hit!')
                # print(f'{security['ticker']} IN RANGE!!!!!! {index}/{len(watchlist)}')
                # candle_object.chart(120)
                # print(hits)
            else:
                print(str(index) + '/' + str(len(watchlist)))
        except ValueError:
            continue

    sectors = {}
    for security in hits:
        if security['industry'] not in sectors.keys():
            sectors[security['industry']] = 1
        else:
            sectors[security['industry']] += 1
    print(sectors)


dailyscanner('4w-UPwatchlist.json', '>')
dailyscanner('8w-UPwatchlist.json', '>')
