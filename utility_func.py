from candlestick import *
from time import sleep
import finnhub
import json

def expand_data(json_in, json_out):
    #'superstrong-uptrend03-20-21.json'
    with open(json_in) as infile:
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        stocks = json.load(infile)

        stock_list_expanded = []
        for index, stock in enumerate(stocks):
            try:
                industry = finnhub_client.company_profile2(symbol=stock)['finnhubIndustry']
                peers = finnhub_client.company_peers(stock)

                hashable_peers = []
                for peer in peers:
                    hashable_peer = '$' + peer
                    hashable_peers.append(hashable_peer)

                stock_dict = {}
                stock_dict['ticker'] = stock
                stock_dict['industry'] = industry
                stock_dict['peers'] = hashable_peers[:3]
                stock_dict['peers'].append('$SPY')
                stock_list_expanded.append(stock_dict)

                print(index)
                print(stock_dict)
                sleep(1)
            except KeyError:
                continue
        #'dict-superstrong-uptrend03-20-21.json'
        with open(json_out) as outfile:
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

with open('superstrong-uptrend03-20-21.json') as infile:
    super_stocks = json.load(infile)

superstrong_stock_optimal_bollinger_params = {}
for ticker in super_stocks:
    try:
        bb_window, bb_std = optimal_bb_window_and_stddev(ticker)
        print(f'\n\n Rolling Window: {bb_window}, STD: {bb_std}')
        superstrong_stock_optimal_bollinger_params[ticker] = [bb_window, bb_std]
    except:
        continue

with open('superstrong_bb_params.json', 'w') as outfile:
    json.load(superstrong_stock_optimal_bollinger_params, outfile, indent=2)
#
# test = DailyCandleDataRT('BBW', 365, 20, 2)
# test.chart(120)
# # print(test.df)
# # print(test.entry_counter('>'))
# bb_window, bb_std = optimal_bb_window_and_stddev('BBW')
# print(bb_window, bb_std)
#
# test2 = DailyCandleDataRT('BBW', 365, bb_window, bb_std)
# test2.chart(120)
