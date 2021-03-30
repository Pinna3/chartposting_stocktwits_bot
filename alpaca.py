import requests, json, time
from config import APCA_API_KEY_ID_PAPER, APCA_API_SECRET_KEY_PAPER, HEADERS_PAPER

APCA_API_BASE_URL =  'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(APCA_API_BASE_URL)
POSITIONS_URL = '{}/v2/positions'.format(APCA_API_BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(APCA_API_BASE_URL)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

def get_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

def buy_market(symbol, qty):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': 'buy',
        'type': 'market',
        'time_in_force': 'day'
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS_PAPER)
    return json.loads(r.content)



def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

response = buy_market('AAPL', 1)
time.sleep(1)
print(get_positions())

# 'id': '2dbce402-d724-4005-b3fc-66b7052406eb'
# response = create_order('MSFT', 100, 'buy', 'market', 'day')
# 'id': '172c6770-4740-429f-954e-47f1af20ebe5'
# print(response)

































#return candlestick bar data from num_bars to now
# def return_candles_json(csv_stocklist, period='day', num_bars=365):
def return_candles_json(symbol, period='1Day', num_bars=365):
    daily_bars_url_v1 = '{}/{}?symbols={}&limit={}'.format(config.BARS_URL, period, symbol, num_bars)
    daily_bars_url_v2 = 'https://data.alpaca.markets/v2/stocks/{}/bars?limit={}&timeframe={}'.format(symbol, num_bars, period)
    r = requests.get(daily_bars_url_v1, headers=config.HEADERS_PAPER)
    data = r.json()
    # df = pd.DataFrame(data)
    return data

###Candlesticks stuff, save for later
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
