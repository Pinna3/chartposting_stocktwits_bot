from candlestick import *
from time import sleep
import finnhub
import json
import functools

def make_tickers_consumable(json_in, json_out):
    #'superstrong-uptrend03-20-21.json'
    with open(json_in) as infile:
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        stocks = json.load(infile)

        stock_list_expanded = []
        for stock in stocks:
            try:
                print(stock)
                industry = finnhub_client.company_profile2(symbol=stock)['finnhubIndustry']
                sleep(1)
                peers = finnhub_client.company_peers(stock)
                sleep(1)
                bb_window, bb_std = optimal_bb_window_and_stddev(stock)
                print(f'Rolling Window: {bb_window}, STD: {bb_std}\n\n')

                hashable_peers = []
                for peer in peers:
                    hashable_peer = '$' + peer
                    hashable_peers.append(hashable_peer)

                stock_dict = {}
                stock_dict['ticker'] = stock
                stock_dict['industry'] = industry
                stock_dict['bb_window'] = bb_window
                stock_dict['bb_std'] = bb_std
                stock_dict['peers'] = hashable_peers[:3]
                stock_dict['peers'].append('$SPY')
                stock_list_expanded.append(stock_dict)

                print(stock_dict)
            except:
                continue
        #'dict-superstrong-uptrend03-20-21.json'
        with open(json_out, 'w') as outfile:
            json.dump(stock_list_expanded, outfile, indent=2)
# expand_data('superstrong-uptrend03-20-21.json', 'dict-superstrong-uptrend03-20-21.json')


def optimal_bb_window_and_stddev(ticker):
    def optimal_bb_window(ticker):
        # print('rolling window, [entries, entry duration]')
        rolling_window_and_counter = []
        for rolling_window in range(13):
            try:
                time.sleep(1)
                rolling_window_and_counter.append([rolling_window, \
                    DailyCandleDataRT(ticker, 365, rolling_window, 1).entry_counter('>')])
                print(rolling_window_and_counter[rolling_window])
            except:
                continue

        print('')
        # print(rolling_window_and_counter)
        for counter in rolling_window_and_counter:
            # print(counter)
            if counter[1][0] == 12:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] == 11:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] == 10:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] == 9:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] == 8:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] == 7:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return std
            elif counter[1][0] == 6:
                # print(counter[0], counter[1])
                rolling_window = counter[0]
                return std
        return None

    def optimal_bb_std(ticker, rolling_window):
        ###### COPY ALGO FROM ABOVE
        # print('std, [entries, entry duration]')
        std_and_counter = []
        for index, std in enumerate([.2, .4, .6, .8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]):
            try:
                time.sleep(1)
                std_and_counter.append([std, DailyCandleDataRT(ticker, 365, rolling_window, std).entry_counter('>')])
                print(std_and_counter[index])
            except:
                continue

        print('')
        for counter in std_and_counter:
            if counter[1][0] == 12:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 11:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 10:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 9:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 8:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 7:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
            elif counter[1][0] == 6:
                # print(counter[0], counter[1])
                std = counter[0]
                return std
        return None

    bb_window = optimal_bb_window(ticker)
    bb_std = optimal_bb_std(ticker, bb_window)
    return bb_window, bb_std

def memoize(function):
    function._cache = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in function._cache:
            function._cache[key] = function(*args, **kwargs)
        return function._cache[key]
    return wrapper

# make_tickers_consumable('test_tickers.json', 'ticker_dict.json')
