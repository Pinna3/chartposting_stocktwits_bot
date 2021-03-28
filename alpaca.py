import config, requests, json, time
import pandas as pd


def return_candles_json(csv_stocklist, period='day', num_bars=1000):
    daily_bars_url = '{}/{}?symbols={}&limit={}'.format(config.BARS_URL, period, csv_stocklist, num_bars)
    r = requests.get(daily_bars_url, headers=config.HEADERS)
    data = r.json()
    # df = pd.DataFrame(data)
    return data

with open('StockLists/VeryLargeStocks$4B+.csv') as infile:
    stocks = infile.readlines()

symbols = [stock.split(',')[0].strip() for stock in stocks[1:]]

#15 allows us to handle up to 3000 stocks without complications
batch = len(symbols) // 15
remainder = len(symbols) % 15

json_candle_batches_pair_with_reference_keys = []
remainder_reference = symbols[-remainder:]
remainder_batch = ','.join(remainder_reference)
for batch_num in range(1, 16):
    symbol_reference = symbols[(batch_num - 1)*batch: batch_num*batch]
    symbol_batch = ','.join(symbol_reference)
    batch_data = return_candles_json(symbol_batch, period='day', num_bars=1000)
    json_candle_batches_pair_with_reference_keys.append([batch_data, symbol_reference])
remainder_data = return_candles_json(remainder_batch, period='day', num_bars=1000)

# print(pd.DataFrame(remainder_data[0]))
# print(pd.DataFrame(remainder_data[remainder_reference[0]]))


for reference_symbol in remainder_reference:
    print(pd.DataFrame(remainder_data[reference_symbol]))

for pair in json_candle_batches_pair_with_reference_keys[0]:
    print(pd.DataFrame(pair[0][pair[1]]))
