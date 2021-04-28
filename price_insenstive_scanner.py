# pylint: disable=no-name-in-module
# pylint: disable=import-error
# pylint: disable=undefined-variable
# pylint: disable=function-redefined
# pylint: disable=unused-wildcard-import
from utility_func import*
from alpaca import*
from tweet import twitter_api


def daily_trader(publish=False):
    watchlist_dict = curate_watchlist()
    dict_length = 0
    for dir in ['>', '<']:
        for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
            dict_length += len(watchlist_dict[dir][mktcap])
    pprint(watchlist_dict)
    print('')
    print_daily_counter_capacities()
    for direction in ['up', 'down']:
        for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
            print(direction, mktcap, yield_first_nonzero_dropoff_tuple_below_threshold(
                mktcap, direction, 80, interval=5, dr_threshold=.33, percent_of_total_threshold=.25))
    print('')
    print('Position Count:', len(get_all_positions()))
    print('')
    sleep(.7)

    sector_allocation_dict = initialize_sector_allocation_dict()

    liquidate_open_positions_without_attached_trailing_stops()

    # UPTRENDS
    for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
        for security in watchlist_dict['>'][mktcap]:
            ticker = security[0]
            print(ticker + '/' + str(dict_length))
            current_price = get_current_open_market_price(ticker, '>')
            sleep(.7)
            if ticker not in get_all_portfolio_tickers():
                sleep(.7)
                sector = fetch_sector(ticker)
                candle_object = SecurityTradeData(ticker, num_of_periods=201)
                atr = candle_object.df.iloc[-1][-1]

                def main(ticker, sector, sector_allocation_dict, mktcap):
                    long_cap = check_long_capacity(
                        sector_allocation_dict['long']['acct_percentage'])
                    daily_counter_cap = check_daily_counter_capacity(
                        'long', mktcap)
                    if not long_cap and not daily_counter_cap:
                        if sector in sector_allocation_dict['long']['sector'].keys():
                            sector_cap = sector_capacity(
                                sector_allocation_dict['long']['sector'][sector]['acct_percentage'], max_exposure=20)
                        else:
                            sector_cap = False
                        if not sector_cap:
                            if not check_daily_tradelist(ticker):
                                price = current_price
                                if price == 0:
                                    return False
                                else:
                                    acct_value = get_account_value()
                                    sleep(.7)
                                    qty = (acct_value / 100) // float(price)
                                    try:
                                        market_order_id = buy_market(
                                            ticker, qty)['id']
                                        sleep(.7)
                                    except KeyError:
                                        print(
                                            f"MISSED ORDER......... TICKER: {ticker}")
                                        print(buy_market(ticker, qty))
                                        sleep(.7)
                                        return False

                                    order = get_order_by_id(market_order_id)
                                    sleep(.7)

                                    order_qty = order['qty']
                                    filled = None
                                    while filled is None:
                                        filled = get_order_by_id(market_order_id)[
                                            'filled_qty']
                                        sleep(.7)
                                        if filled != order_qty:
                                            filled = None
                                            continue

                                    market_order_fill_price = None
                                    while market_order_fill_price is None:
                                        market_order_fill_price = round(
                                            float(get_order_by_id(market_order_id)['filled_avg_price']), 2)
                                        sleep(.7)

                                    trailing_percentage = (
                                        atr / market_order_fill_price) * 100
                                    tstop_order_id = trailing_stop_long(
                                        ticker, trailing_percentage)['id']
                                    sleep(.7)
                                    tstop_stop_price = None
                                    while tstop_stop_price is None:
                                        tstop_stop_price = round(
                                            float(get_order_by_id(tstop_order_id)['stop_price']), 2)
                                        sleep(.7)

                                    add_to_daily_counter('long', mktcap)
                                    add_to_daily_tradelist(ticker)
                                    sector_allocation_dict = initialize_sector_allocation_dict()
                                    print(
                                        f"TRADE PLACED..... {ticker}: Current Price: {current_price}, Trade Price: {market_order_fill_price} \nStop Price: {tstop_stop_price} MktGroup: {mktcap}\n")
                                    return True
                            else:
                                print(
                                    f'{ticker} TRADE NOT PLACED... No Duplicate Trades')
                                return False
                        else:
                            print(
                                f'{ticker} TRADE NOT PLACED... Sector At Capacity')
                            return False
                    else:
                        print(
                            f'{ticker} TRADE NOT PLACED... Long/Daily Capacity Hit')
                        return False

                if publish:
                    execution = main(
                        ticker, sector, sector_allocation_dict, mktcap)
                    if execution:
                        chart = candle_object.chart(
                            120, '>', destination='twitter')
                        media = twitter_api.media_upload(
                            filename='image/png', file=chart)
                        peers = fetch_peers(ticker)
                        tweet = f'''${ticker} Trade Alert\n\nType: Long, Momentum\nSector: {sector}\nPeers: {peers}'''
                        twitter_api.update_status(
                            tweet, media_ids=[media.media_id])
                else:
                    main(ticker, sector, sector_allocation_dict, mktcap)

        for security in watchlist_dict['<'][mktcap]:
            ticker = security[0]
            print(ticker + '/' + str(dict_length))
            current_price = get_current_open_market_price(ticker, '<')
            sleep(.7)
            if ticker not in get_all_portfolio_tickers():
                sleep(.7)
                sector = fetch_sector(ticker)
                candle_object = SecurityTradeData(ticker, num_of_periods=201)
                atr = candle_object.df.iloc[-1][-1]

                def main(ticker, sector, sector_allocation_dict, mktcap):
                    short_cap = check_short_capacity(
                        sector_allocation_dict['short']['acct_percentage'])
                    daily_counter_cap = check_daily_counter_capacity(
                        'short', mktcap)
                    if not short_cap and not daily_counter_cap:
                        if sector in sector_allocation_dict['short']['sector'].keys():
                            sector_cap = sector_capacity(
                                sector_allocation_dict['short']['sector'][sector]['acct_percentage'], max_exposure=20)
                        else:
                            sector_cap = False
                        if not sector_cap:
                            if not check_daily_tradelist(ticker):
                                price = current_price
                                if price == 0:
                                    return False
                                else:
                                    acct_value = get_account_value()
                                    sleep(.7)
                                    qty = (acct_value / 100) // float(price)
                                    try:
                                        market_order_id = sell_market(
                                            ticker, qty)['id']
                                        sleep(.7)
                                    except KeyError:
                                        print(
                                            f"MISSED ORDER......... TICKER: {ticker}")
                                        print(sell_market(ticker, qty))
                                        sleep(.7)
                                        return False

                                    order = get_order_by_id(market_order_id)
                                    sleep(.7)

                                    order_qty = order['qty']
                                    filled = None
                                    while filled is None:
                                        filled = get_order_by_id(market_order_id)[
                                            'filled_qty']
                                        sleep(.7)
                                        if filled != order_qty:
                                            filled = None
                                            continue

                                    market_order_fill_price = None
                                    while market_order_fill_price is None:
                                        market_order_fill_price = round(
                                            float(get_order_by_id(market_order_id)['filled_avg_price']), 2)
                                        sleep(.7)

                                    trailing_percentage = (
                                        atr / market_order_fill_price) * 100
                                    tstop_order_id = trailing_stop_short(
                                        ticker, trailing_percentage)['id']
                                    sleep(.7)
                                    tstop_stop_price = None
                                    while tstop_stop_price is None:
                                        tstop_stop_price = round(
                                            float(get_order_by_id(tstop_order_id)['stop_price']), 2)
                                        sleep(.7)

                                    add_to_daily_counter('short', mktcap)
                                    add_to_daily_tradelist(ticker)
                                    sector_allocation_dict = initialize_sector_allocation_dict()
                                    print(
                                        f"TRADE PLACED..... {ticker}: Current Price: {current_price}, Trade Price: {market_order_fill_price} \nStop Price: {tstop_stop_price} MktGroup: {mktcap}\n")
                                    return True
                            else:
                                print(
                                    f'{ticker} TRADE NOT PLACED... No Duplicate Trades')
                                return False
                        else:
                            print(
                                f'{ticker} TRADE NOT PLACED... Sector At Capacity')
                            return False
                    else:
                        print(
                            f'{ticker} TRADE NOT PLACED... Short/Daily Capacity Hit')
                        return False

                if publish:
                    execution = main(
                        ticker, sector, sector_allocation_dict, mktcap)
                    if execution:
                        chart = candle_object.chart(
                            120, '<', destination='twitter')
                        media = twitter_api.media_upload(
                            filename='image/png', file=chart)
                        peers = fetch_peers(ticker)
                        tweet = f'''${ticker} Trade Alert\n\nType: Short, Momentum\nSector: {sector}\nPeers: {peers}'''
                        twitter_api.update_status(
                            tweet, media_ids=[media.media_id])
                else:
                    main(ticker, sector, sector_allocation_dict, mktcap)
