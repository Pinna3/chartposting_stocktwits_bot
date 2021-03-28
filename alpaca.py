import config, requests, json#, time
import pandas as pd

#return candlestick bar data from num_bars to now
# def return_candles_json(csv_stocklist, period='day', num_bars=365):
def return_candles_json(symbol, period='1Day', num_bars=365):
    daily_bars_url_v1 = '{}/{}?symbols={}&limit={}'.format(config.BARS_URL, period, symbol, num_bars)
    daily_bars_url_v2 = 'https://data.alpaca.markets/v2/stocks/{}/bars?limit={}&timeframe={}'.format(symbol, num_bars, period)
    r = requests.get(daily_bars_url_v1, headers=config.HEADERS_PAPER)
    data = r.json()
    # df = pd.DataFrame(data)
    return data

# with open('StockLists/VeryLargeStocks$4B+.csv') as infile:
#     stocks = infile.readlines()
#
# symbols = [stock.split(',')[0].strip() for stock in stocks[1:]]
#
# #15 allows us to handle up to 3000 stocks without complications
# batch = len(symbols) // 15
# remainder = len(symbols) % 15
#
# # #remainder batch dataframe conversion
# # remainder_reference = symbols[-remainder:]
# # remainder_batch = ','.join(remainder_reference)
# # remainder_data = return_candles_json(remainder_batch, period='day', num_bars=1000)
# # for reference_symbol in remainder_reference:
# #     print(pd.DataFrame(remainder_data[reference_symbol]))
#
# json_candle_batches_pair_with_reference_keys = []
# # for batch_num in range(1, 16):
# for batch_num in range(1, 2):
#     symbol_reference = symbols[(batch_num - 1)*batch: batch_num*batch]
#     symbol_batch = ','.join(symbol_reference)
#     batch_data = return_candles_json(symbol_batch, period='day', num_bars=1000)
#     # print(len(batch_data))
#     json_candle_batches_pair_with_reference_keys.append([batch_data, symbol_reference])
#     # print(len(json_candle_batches_pair_with_reference_keys[0][1]))
#
#
#
#
#
# for pair in json_candle_batches_pair_with_reference_keys:
#     # print(len(pair))
#     index = pair[1]
#     print(pd.DataFrame(pair[0][index]))
