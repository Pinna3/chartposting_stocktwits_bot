from candlestick import SecurityTradeData
from time import sleep
import finnhub
from tweet import twitter_api
import json
import operator
from alpaca import get_quote, buy_market, get_account, trailing_stop_long, sell_market, trailing_stop_short
from utility_func import initialize_holdings
from risk_parameter import*
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

    holdings = initialize_holdings()
    print(holdings)
    missed_connection = []
    missed_candle_object_error = []
    missed_chart_error = []
    missed_order_error = []

    #loop through securities and filter for up/down trends
    for index, security in enumerate(watchlist):
        try:
            try:
                candle_object = SecurityTradeData(security['ticker'], 365)
            except ValueError:
                    try:
                        candle_object = SecurityTradeData(security['ticker'], 265)
                    except ValueError:
                        missed_candle_object_error.append(security['ticker'])
                        print(f'MISSED CANDLE OBJECT ERROR!!!!...{missed_candle_object_error}')
                        continue
            candle_object.custom_bollingers(security['bb_window'], security['bb_std'])
            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-1]
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
                                missed_chart_error.append(security['ticker'])
                                print(f'MISSED CHART!!!!...{missed_chart_error}')
                                continue

                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Long, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            holdings = initialize_holdings()
                            print(holdings)
                        else:
                            print(f"Long Capacity: {long_capacity(holdings['long']['acct_percentage'])}")
                            print(f"Daily Counter Capacity: {check_daily_counter_capacity('long', security['mktcap'])}")
                            if long_capacity(holdings['long']['acct_percentage']) is False and \
                                check_daily_counter_capacity('long', security['mktcap']) is False:
                                if security['industry'] in holdings['long']['industry'].keys():
                                    industry_capacity = industry_capacity(holdings['long']['industry'][security['industry']]['acct_percentage'])
                                else:
                                    industry_capacity = False
                                print(f"Industry Capacity: {industry_capacity}")
                                if industry_capacity is False:
                                    # price = get_quote(security['ticker'])['last']['askprice']
                                    # acct_value = get_account_value()
                                    # try:
                                    #     qty = (acct_value / 100) // float(price)
                                    # except ZeroDivisionError:
                                    #     missed_order_error.append(security['ticker'])
                                    #     print(f'MISSED ORDER ERROR!!!!...{missed_order_error}')
                                    #     continue
                                    # buy_market(security['ticker'], qty)
                                    # sleep(3)
                                    # trailing_stop_long(security['ticker'], 2.0)
                                    add_to_daily_counter('long', security['mktcap'])
                                    holdings = initialize_holdings()
                                    print(holdings)
                                else:
                                    print(f'At Capacity At Capacity At Capacity At Capacity')
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
                                missed_candle_object_error.append(security['ticker'])
                                print(f'MISSED!!!!...{missed_candle_object_error}')
                                continue

                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Short, Momentum\nIndustry: {security['industry']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            holdings = initialize_holdings()
                            print(holdings)
                        else:
                            print(f"Short Capacity: {short_capacity(holdings['short']['acct_percentage'])}")
                            print(f"Daily Counter Capacity: {check_daily_counter_capacity('short', security['mktcap'])}")
                            if short_capacity(holdings['short']['acct_percentage']) is False and \
                                check_daily_counter_capacity('short', security['mktcap']) is False:
                                if security['industry'] in holdings['short']['industry'].keys():
                                    industry_capacity = industry_capacity(holdings['short']['industry'][security['industry']]['acct_percentage'])
                                else:
                                    industry_capacity = False
                                print(f"Industry Capacity: {industry_capacity}")
                                if industry_capacity is False:
                                    # price = get_quote(security['ticker'])['last']['askprice']
                                    # acct_value = get_account_value()
                                    # try:
                                    #     qty = (acct_value / 100) // float(price)
                                    # except ZeroDivisionError:
                                    #     missed_order_error.append(security['ticker'])
                                    #     print(f'MISSED!!!!...{missed_order_error}')
                                    #     continue
                                    # sell_market(security['ticker'], qty)
                                    # sleep(3)
                                    # trailing_stop_short(security['ticker'], 2.0)
                                    add_to_daily_counter('short', security['mktcap'])
                                    holdings = initialize_holdings()
                                    print(holdings)
                                else:
                                    print(f'At Capacity At Capacity At Capacity At Capacity')
                    else:
                        print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))
        except:
            missed_connection.append(security['ticker'])
            print(f'ConnectionError...{missed_connection}')
            continue

while True:
    # #longs 70%
    # dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(20,)D-6E-uptrend03-29-21.json', '>', publish=False)
    # dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('LargeStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('LargeStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('LargeStocks/Watchlists/03-29-21/(45,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('MediumStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('MediumStocks/Watchlists/03-29-21/(25,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('MediumStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('SmallStocks/Watchlists/03-29-21/(45,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('SmallStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('SmallStocks/Watchlists/03-29-21/(30,)D-6E-uptrend03-29-21.json', '>', publish=False)
    dailyscanner('MicroStocks/Watchlists/03-29-21/(5,)D-6E-uptrend03-29-21.json', '>', publish=False)

    #shorts 30%
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(15,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('VeryLargeStocks/Watchlists/03-29-21/(20,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('LargeStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('LargeStocks/Watchlists/03-29-21/(15,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('MediumStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('SmallStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
    dailyscanner('MicroStocks/Watchlists/03-29-21/(10,)D-6E-downtrend03-29-21.json', '<', publish=False)
