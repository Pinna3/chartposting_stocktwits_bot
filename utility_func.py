from candlestick import DailyCandleDataRT
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



test = DailyCandleDataRT('PSP', 365, 20, 2)
test.chart(120)
print(test.df)
# print(test.entry_counter('>'))



print('rolling window, [entries, entry duration]')
rolling_window_and_counter = []
for rolling_window in range(12):
    try:
        time.sleep(1)
        rolling_window_and_counter.append([rolling_window, \
            DailyCandleDataRT('PSP', 365, rolling_window, 1).entry_counter('>')])
        print(rolling_window_and_counter[rolling_window])
    except:
        continue

print('')
for counter in rolling_window_and_counter:
    if counter[1][0] == 12:
        print(counter[0], counter[1])
        rolling_window = counter[0]
        break
    elif counter[1][0] == 11:
        print(counter[0], counter[1])
        rolling_window = counter[0]
        break
    elif counter[1][0] == 10:
        print(counter[0], counter[1])
        rolling_window = counter[0]
        break
    elif counter[1][0] == 9:
        print(counter[0], counter[1])
        rolling_window = counter[0]
        break
    elif counter[1][0] == 8:
        print(counter[0], counter[1])
        rolling_window = counter[0]
        break
    else:
        print('No match.')
print(f'Optimal Rolling Window = {rolling_window}\n\n')


###### COPY ALGO FROM ABOVE
print('std, [entries, entry duration]')
std_and_counter = []
for index, std in enumerate([.2, .4, .6, .8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4]):
    try:
        time.sleep(1)
        std_and_counter.append([std, DailyCandleDataRT('PSP', 365, rolling_window, std).entry_counter('>')])
        print(std_and_counter[index])
    except:
        continue

print('')
for counter in std_and_counter:
    if counter[1][0] == 12:
        print(counter[0], counter[1])
        std = counter[0]
        break
    elif counter[1][0] == 11:
        print(counter[0], counter[1])
        std = counter[0]
        break
    elif counter[1][0] == 10:
        print(counter[0], counter[1])
        std = counter[0]
        break
    elif counter[1][0] == 9:
        print(counter[0], counter[1])
        std = counter[0]
        break
    elif counter[1][0] == 8:
        print(counter[0], counter[1])
        std = counter[0]
        break
    else:
        print('No match.')
print(f'Optimal Standard Deviation = {std}\n\n')

DailyCandleDataRT('PSP', 365, rolling_window, std).chart(120)
