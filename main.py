from candlestick import SecurityTradeData
from time import sleep
import finnhub
from tweet import twitter_api
import json
import operator
from alpaca import get_quote, buy_market, get_account, trailing_stop_long, sell_market, trailing_stop_short
from utility_func import initialize_holdings, drop_off_based_watchlist_filter, pull_top_tier_unbroken_trenders
from risk_parameter import*
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')


def dailyscanner(json_watchlist, op_str, watchlist_date, publish=False):
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
        # try:
            try:
                candle_object = SecurityTradeData(security['ticker'])
            except ValueError:
                    try:
                        candle_object = SecurityTradeData(security['ticker'], num_days=265)
                    except ValueError:
                        missed_candle_object_error.append(security['ticker'])
                        print(f'MISSED CANDLE OBJECT ERROR!!!!...{missed_candle_object_error}')
                        continue
            candle_object.custom_bollingers(security['bb_window'], security['bb_std'])
            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle_object.df.iloc[-1]
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
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Long, Momentum\nSector: {security['sector']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            holdings = initialize_holdings()
                            print(holdings)
                        else:
                            long_cap = long_capacity(holdings['long']['acct_percentage'], watchlists_generation_date=watchlist_date)
                            print(f"Long Capacity: {long_cap}")
                            daily_counter_cap = check_daily_counter_capacity('long', security['mktcap'], watchlists_generation_date=watchlist_date)
                            print(f"Daily Counter Capacity: {daily_counter_cap}")
                            if long_cap is False and \
                                daily_counter_cap is False:
                                if security['sector'] in holdings['long']['sector'].keys():
                                    sector_cap = sector_capacity(holdings['long']['sector'][security['sector']]['acct_percentage'])
                                else:
                                    sector_cap = False
                                if sector_cap is False:
                                    if check_daily_tradelist(security['ticker']) == False:
                                        price = get_quote(security['ticker'])['last']['askprice']
                                        acct_value = get_account_value()
                                        try:
                                            qty = (acct_value / 100) // float(price)
                                        except ZeroDivisionError:
                                            missed_order_error.append(security['ticker'])
                                            print(f'MISSED ORDER ERROR!!!!...{missed_order_error}')
                                            continue
                                        buy_market(security['ticker'], qty)
                                        sleep(3)
                                        trailing_stop_long(security['ticker'], atr)
                                        add_to_daily_counter('long', security['mktcap'])
                                        holdings = initialize_holdings()
                                        print(holdings)
                                        candle_object.chart(120)
                                    else:
                                        print('No Duplicate Trades No Duplicate Trades No Duplicate Trades')
                                else:
                                    print(f'At Capacity At Capacity At Capacity At Capacity')
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
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Short, Momentum\nSector: {security['sector']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            holdings = initialize_holdings()
                            print(holdings)
                        else:
                            short_cap = short_capacity(holdings['short']['acct_percentage'], watchlists_generation_date=watchlist_date)
                            print(f"Short Capacity: {short_cap}")
                            daily_counter_cap = check_daily_counter_capacity('short', security['mktcap'], watchlists_generation_date=watchlist_date)
                            print(f"Daily Counter Capacity: {daily_counter_cap}")
                            if short_cap is False and \
                                daily_counter_cap is False:
                                if security['sector'] in holdings['short']['sector'].keys():
                                    sector_cap = sector_capacity(holdings['short']['sector'][security['sector']]['acct_percentage'])
                                else:
                                    sector_cap = False
                                print(f"Sector Capacity: {sector_capacity}")
                                if sector_cap is False:
                                    if check_daily_tradelist(security['ticker']) == False:
                                        price = get_quote(security['ticker'])['last']['askprice']
                                        acct_value = get_account_value()
                                        try:
                                            qty = (acct_value / 100) // float(price)
                                        except ZeroDivisionError:
                                            missed_order_error.append(security['ticker'])
                                            print(f'MISSED!!!!...{missed_order_error}')
                                            continue
                                        sell_market(security['ticker'], qty)
                                        sleep(3)
                                        trailing_stop_short(security['ticker'], atr)
                                        add_to_daily_counter('short', security['mktcap'])
                                        holdings = initialize_holdings()
                                        print(holdings)
                                        candle_object.chart(120)
                                    else:
                                        print('No Duplicate Trades No Duplicate Trades No Duplicate Trades')
                                else:
                                    print(f'At Capacity At Capacity At Capacity At Capacity')
                            else:
                                print(f'At Capacity At Capacity At Capacity At Capacity')
                    else:
                        print(security['ticker'] + ' ' + str(index) + '/' + str(len(watchlist)))
        # except:
        #     missed_connection.append(security['ticker'])
        #     print(f'ConnectionError...{missed_connection}')
        #     continue


watchlists_generation_date = '04-04-21'
while True:
    # ###Think about another filtering mechanism (worried about shorts) (maybe restrict to long trending or winning trend, feels off)
    # print('.')
    # print('.')
    # print('.')
    # [print(item[0]) for item in pull_top_tier_unbroken_trenders(watchlists_generation_date, tier_percentage=10)]
    # print('.')
    # print('.')
    # print('.')
    # for filename, direction, number, total in pull_top_tier_unbroken_trenders(watchlists_generation_date, tier_percentage=10):
    #     print('')
    #     print(filename)
    #     print('')
    #     dailyscanner(filename, direction, watchlist_date=watchlists_generation_date, publish=False)
    print('.')
    print('.')
    print('.')
    [print(item[0]) for item in drop_off_based_watchlist_filter(watchlists_generation_date, max_per_category=3, drop_off_rate_cutoff=.25)]
    print('.')
    print('.')
    print('.')
    for filename, direction in drop_off_based_watchlist_filter(watchlists_generation_date, max_per_category=3, drop_off_rate_cutoff=.25):
        print('')
        print(filename)
        print('')
        dailyscanner(filename, direction, watchlist_date=watchlists_generation_date, publish=False)
