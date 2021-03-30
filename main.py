from candlestick import SecurityTradeData
from time import sleep
import finnhub
from tweet import twitter_api
import json
import operator
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')


def dailyscanner(json_watchlist, op_str, publish=False):
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
    for index, security in enumerate(watchlist):
        try:
            candle_object = SecurityTradeData(security['ticker'], 365)
            candle_object.custom_bollingers(security['bb_window'], security['bb_std'])
            c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-1]
            if op_str == '>':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    opposite_op_func(c, lower):
                    hit = {'ticker': security['ticker'], 'industry': security['industry'], 'direction': 'long'}
                    if hit not in hits:
                        hits.append(hit)
                        try:
                            candle_object.chart(120, destination=security['mktcap'])
                        except FileNotFoundError:
                            security['mktcap'] = 'VeryLarge'
                            candle_object.chart(120, destination=security['mktcap'])
                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Long, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            print(hits)
                        else:
                            print(hits)
                else:
                    print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))

            elif op_str == '<':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    opposite_op_func(c, upper):
                    hit = {'ticker': security['ticker'], 'industry': security['industry'], 'direction': 'short'}
                    if hit not in hits:
                        hits.append(hit)
                        #Some market caps showing up null... keep an eye on
                        try:
                            candle_object.chart(120, destination=security['mktcap'])
                        except FileNotFoundError:
                            security['mktcap'] = 'VeryLarge'
                            candle_object.chart(120, destination=security['mktcap'])
                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Short, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            print(hits)
                        else:
                            print(hits)
                else:
                    print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))
        except:
            continue

    sectors = {}
    for security in hits:
        if security['industry'] not in sectors.keys():
            sectors[security['industry']] = 1
        else:
            sectors[security['industry']] += 1
    print(sectors)


hits = []
# # while True:
# #longs 70%
dailyscanner('VeryLargeStocks/(30,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('VeryLargeStocks/(20,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('VeryLargeStocks/(5,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('LargeStocks/(30,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('LargeStocks/(25,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('LargeStocks/(20,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('LargeStocks/(5,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('MediumStocks/(30,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('MediumStocks/(25,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('MediumStocks/(20,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('MediumStocks/(5,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('SmallStocks/(5,)D-uptrend03-28-21.json', '>', publish=True)
dailyscanner('MicroStocks/(5,)D-uptrend03-28-21.json', '>', publish=True)

#shorts 30%
dailyscanner('VeryLargeStocks/(10,)D-downtrend03-28-21.json', '<', publish=True)
dailyscanner('LargeStocks/(10,)D-downtrend03-28-21.json', '<', publish=True)
dailyscanner('MediumStocks/(10,)D-downtrend03-28-21.json', '<', publish=True)
dailyscanner('MicroStocks/(5,)D-downtrend03-28-21.json', '<', publish=True)

# shop = SecurityTradeData('SHOP', 365)
# shop.chart(120, destination='VeryLarge')
#
# media = twitter_api.media_upload('VeryLargeStocks/Charts/03-29-21/SHOP.png')
# tweet = '$SHOP Below 200SMA'
#
# twitter_api.update_status(tweet, media_ids=[media.media_id])
