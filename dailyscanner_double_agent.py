from candlestick import SecurityTradeData
from time import sleep
import finnhub
from tweet import twitter_api
import json
import operator
from alpaca import get_quote, buy_market, get_account, trailing_stop_long, sell_market, trailing_stop_short, get_last_trade, get_order_by_id, get_current_open_market_price
from utility_func import initialize_sector_allocation_dict, drop_off_based_watchlist_filter
from risk_parameter import*
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')


def dailyscanner_double_agent(json_watchlist, op_str, publish=False):
    with open(json_watchlist) as infile:
        watchlist = json.load(infile)

    #up/down trendtrend toggle
    ops = {"<": operator.lt, ">": operator.gt}
    op_func = ops[op_str]
    opposite_ops = {">": operator.lt, "<": operator.gt}
    opposite_op_func = opposite_ops[op_str]

    sector_allocation_dict = initialize_sector_allocation_dict()
    missed_connection = []
    missed_candle_object_error = []
    missed_chart_error = []
    missed_order = []

    #loop through securities and filter for up/down trends
    for index, security in enumerate(watchlist):
        # try:
            candle_object = SecurityTradeData(security['ticker'], num_of_periods=201)
            candle_object.sma200_double_agent_activate(security['200sma_double_agent'])
            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle_object.df.iloc[-1]
            #find better way... weak link... slow and innaccurate. (i think the funded keys access more exchanges so this may be a non issue)
            c = get_current_open_market_price(security['ticker'], op_str)
            if op_str == '>':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and opposite_op_func(c, sma200):
                    holding = security['ticker']
                    if holding not in get_all_portfolio_tickers():
                        print(f"BUYING RANGE..... {holding}: Current Price: {c}, 200SMA Double Agent: {sma200}")
                        candle_object.chart(120, destination=security['mktcap'])
                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Long, Momentum\nSector: {security['sector']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            sector_allocation_dict = initialize_sector_allocation_dict()
                        else:
                            long_cap = check_long_capacity(sector_allocation_dict['long']['acct_percentage'])
                            daily_counter_cap = check_daily_counter_capacity('long', security['mktcap'])
                            if long_cap is False and daily_counter_cap is False:
                                if security['sector'] in sector_allocation_dict['long']['sector'].keys():
                                    sector_cap = sector_capacity(sector_allocation_dict['long']['sector'][security['sector']]['acct_percentage'])
                                else:
                                    sector_cap = False
                                if sector_cap is False:
                                    if check_daily_tradelist(security['ticker']) == False:
                                        price = c
                                        if price == 0:
                                            continue
                                        else:
                                            acct_value = get_account_value()
                                            qty = (acct_value / 100) // float(price)
                                            try:
                                                market_order_id = buy_market(security['ticker'], qty)['id']
                                            except KeyError:
                                                missed_order.append(security['ticker'])
                                                print(f"MISSED ORDER......... TICKER: {security['ticker']}")
                                                continue
                                            sleep(2)
                                            market_order_fill_price = round(float(get_order_by_id(market_order_id)['filled_avg_price']), 2)
                                            trailing_percentage = (atr / market_order_fill_price) * 100
                                            #trailing stop only works when marke is open
                                            tstop_order_id = trailing_stop_long(security['ticker'], trailing_percentage)['id']
                                            sleep(2)
                                            tstop_stop_price = round(float(get_order_by_id(tstop_order_id)['stop_price']), 2)
                                            add_to_daily_counter('long', security['mktcap'])
                                            add_to_daily_tradelist(security['ticker'])
                                            sector_allocation_dict = initialize_sector_allocation_dict()
                                            print(f"TRADE PLACED..... {holding}: Current Price: {c}, Trade Price: {market_order_fill_price} \n200SMA Double Agent: {sma200}, Stop Price: {tstop_stop_price} \nMktGroup: {security['mktcap']}\n")
                                    else:
                                        print('TRADE NOT PLACED... No Duplicate Trades')
                                else:
                                    print('TRADE NOT PLACED... Sector At Capacity')
                            else:
                                print('TRADE NOT PLACED... Long/Daily Capacity Hit')
                else:
                    print(security['ticker'] + ' ' + str(index+1) + '/' + str(len(watchlist)))

            elif op_str == '<':
                if op_func(sma9, sma20) and op_func(sma20, sma50) and opposite_op_func(c, sma200):
                    holding = security['ticker']
                    if holding not in get_all_portfolio_tickers():
                        print(f"SHORTING RANGE..... {holding}: Current Price: {c}, 200SMA Double Agent: {sma200}")
                        candle_object.chart(120, destination=security['mktcap'])
                        if publish:
                            media = twitter_api.media_upload(f'''{security['mktcap']}Stocks/Charts/{today_date}/{security['ticker']}.png''')
                            tweet = f'''${security['ticker']} Trade Alert\n\nType: Short, Momentum\nSector: {security['sector']}\nPeers: {' '.join(security['peers'])}'''
                            twitter_api.update_status(tweet, media_ids=[media.media_id])
                            sector_allocation_dict = initialize_sector_allocation_dict()
                        else:
                            short_cap = check_short_capacity(sector_allocation_dict['short']['acct_percentage'])
                            daily_counter_cap = check_daily_counter_capacity('short', security['mktcap'])
                            if short_cap is False and daily_counter_cap is False:
                                if security['sector'] in sector_allocation_dict['short']['sector'].keys():
                                    sector_cap = sector_capacity(sector_allocation_dict['short']['sector'][security['sector']]['acct_percentage'])
                                else:
                                    sector_cap = False
                                if sector_cap is False:
                                    if check_daily_tradelist(security['ticker']) == False:
                                        price = c
                                        if price == 0:
                                            continue
                                        else:
                                            acct_value = get_account_value()
                                            qty = (acct_value / 100) // float(price)
                                            try:
                                                market_order_id = sell_market(security['ticker'], qty)['id']
                                            except KeyError:
                                                missed_order.append(security['ticker'])
                                                print(f"MISSED ORDER......... TICKER: {security['ticker']}")
                                                continue
                                            sleep(2)
                                            market_order_fill_price = round(float(get_order_by_id(market_order_id)['filled_avg_price']), 2)
                                            trailing_percentage = (atr / market_order_fill_price) * 100
                                            # #trailing stop only works when market is open
                                            tstop_order_id = trailing_stop_short(security['ticker'], trailing_percentage)['id']
                                            sleep(2)
                                            tstop_stop_price = round(float(get_order_by_id(tstop_order_id)['stop_price']), 2)
                                            add_to_daily_counter('short', security['mktcap'])
                                            add_to_daily_tradelist(security['ticker'])
                                            sector_allocation_dict = initialize_sector_allocation_dict()
                                            print(f"TRADE PLACED..... {holding}: Current Price: {c}, Trade Price: {market_order_fill_price} \n200SMA Double Agent: {sma200}, Stop Price: {tstop_stop_price} \nMktGroup: {security['mktcap']}\n")
                                    else:
                                        print('TRADE NOT PLACED... No Duplicate Trades')
                                else:
                                    print('TRADE NOT PLACED... Sector At Capacity')
                            else:
                                print('TRADE NOT PLACED... Short/Daily Capacity Hit')
                    else:
                        print(security['ticker'] + ' ' + str(index+1) + '/' + str(len(watchlist)))
        # except:
        #     missed_connection.append(security['ticker'])
        #     print(f'ConnectionError...{missed_connection}')
        #     continue
