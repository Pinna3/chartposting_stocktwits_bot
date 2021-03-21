from candlestick import DailyCandleDataRT
from time import sleep
import finnhub
import json

# finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
#
# # Company Peers
# print(finnhub_client.company_peers('RUTH'))

# # # Company Profile 2
# # print(finnhub_client.company_profile2(symbol='AAPL')['finnhubIndustry'])
#
with open('superstrong-uptrend03-20-21.json') as infile:
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

    with open('dict-superstrong-uptrend03-20-21.json', 'w') as outfile:
        json.dump(stock_list_expanded, outfile, indent=2)
