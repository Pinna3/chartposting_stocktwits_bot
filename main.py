from candlestick import SecurityTradeData
from time import sleep
import finnhub
from tweet import twitter_api
import json
import operator
from alpaca import get_quote, buy_market, get_account, trailing_stop_long, sell_market, trailing_stop_short
from utility_func import initialize_holdings
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
        # try:
            candle_object = SecurityTradeData(security['ticker'], 365)
            candle_object.custom_bollingers(security['bb_window'], security['bb_std'])
            c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-1]
            if op_str == '>':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    opposite_op_func(c, lower):
                    holding = security['ticker']
                    if holding not in str(holdings):
                    #Some market caps showing up null... keep an eye on
                        try:
                            candle_object.chart(120, destination=security['mktcap'])
                        except FileNotFoundError:
                            security['mktcap'] = 'VeryLarge'
                            candle_object.chart(120, destination=security['mktcap'])
                        except ValueError:
                            try:
                                candle_object.chart(60, destination=security['mktcap'])
                            except ValueError:
                                continue

                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Long, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            initialize_holdings()
                            print(holdings)
                        else:
                            price = get_quote(security['ticker'])['last']['askprice']
                            acct = get_account()
                            acct_equity = float(acct['equity'])

                            if acct_equity > 25000:
                                acct_multiplier = float(acct['multiplier']) / 2
                            else:
                                acct_multiplier = float(acct['multiplier'])

                            acct_value = acct_equity * acct_multiplier
                            qty = (acct_value / 100) // price
                            buy_market(security['ticker'], qty)
                            sleep(3)
                            trailing_stop_long(security['ticker'], 2.0)
                            initialize_holdings()
                            print(holdings)
                else:
                    print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))

            elif op_str == '<':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    opposite_op_func(c, upper):
                    holding = security['ticker']
                    if holding not in holdings:
                    #Some market caps showing up null... keep an eye on
                        try:
                            candle_object.chart(120, destination=security['mktcap'])
                        except FileNotFoundError:
                            security['mktcap'] = 'VeryLarge'
                            candle_object.chart(120, destination=security['mktcap'])
                        except ValueError:
                            try:
                                candle_object.chart(60, destination=security['mktcap'])
                            except ValueError:
                                continue

                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Short, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            initialize_holdings()
                            print(holdings)
                        else:
                            price = get_quote(security['ticker'])['last']['askprice']
                            acct = get_account()
                            acct_equity = float(acct['equity'])

                            if acct_equity > 25000:
                                acct_multiplier = float(acct['multiplier']) / 2
                            else:
                                acct_multiplier = float(acct['multiplier'])

                            acct_value = acct_equity * acct_multiplier
                            qty = (acct_value / 100) // price
                            sell_market(security['ticker'], qty)
                            sleep(3)
                            trailing_stop_short(security['ticker'], 2.0)
                            initialize_holdings()
                            print(holdings)
                    else:
                        print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))
        # except:
        #     continue

while True:
    # #longs 70%
    holdings = initialize_holdings()
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(20,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('LargeStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('LargeStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('LargeStocks/Watchlists/03-29-21/(45,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MediumStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MediumStocks/Watchlists/03-29-21/(25,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MediumStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('SmallStocks/Watchlists/03-29-21/(45,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('SmallStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('SmallStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MicroStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    holdings = initialize_holdings()

    #shorts 30%
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(15,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(20,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('LargeStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('LargeStocks/Watchlists/03-29-21/(15,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MediumStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('SmallStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
    dailyscanner('MicroStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    holdings = initialize_holdings()
