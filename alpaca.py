import requests, json, time
from config import APCA_API_KEY_ID_PAPER, APCA_API_SECRET_KEY_PAPER, HEADERS_PAPER, BARS_URL

APCA_API_BASE_URL =  'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(APCA_API_BASE_URL)
POSITIONS_URL = '{}/v2/positions'.format(APCA_API_BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(APCA_API_BASE_URL)

DATA_BASE_URL = 'https://data.alpaca.markets'
QUOTE_URL = '{}/v1/last_quote/stocks'.format(DATA_BASE_URL)


def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

def get_all_positions():
    r = requests.get(POSITIONS_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

def get_position_by_symbol(symbol):
    r = requests.get(POSITIONS_URL + f'/{symbol}', headers=HEADERS_PAPER)
    return json.loads(r.content)

def get_quote(symbol):
    r = requests.get(f'{QUOTE_URL}/{symbol}', headers=HEADERS_PAPER)
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

def sell_market(symbol, qty):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': 'sell',
        'type': 'market',
        'time_in_force': 'gtc'
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS_PAPER)
    return json.loads(r.content)

def trailing_stop_long(symbol, percentage):
    qty = get_position_by_symbol(symbol)['qty']
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': 'sell',
        'type': 'trailing_stop',
        'trail_percent': percentage,
        'time_in_force': 'gtc'
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS_PAPER)
    return json.loads(r.content)

def trailing_stop_short(symbol, percentage):
    qty = -float(get_position_by_symbol(symbol)['qty'])
    data = {
        'symbol': symbol,
        'qty': str(qty),
        'side': 'buy',
        'type': 'trailing_stop',
        'trail_percent': percentage,
        'time_in_force': 'gtc'
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS_PAPER)
    return json.loads(r.content)


def get_orders():
    r = requests.get(ORDERS_URL, headers=HEADERS_PAPER)
    return json.loads(r.content)

def get_account_value():
    acct = get_account()
    acct_equity = float(acct['equity'])
    if acct_equity > 25000:
        acct_multiplier = float(acct['multiplier']) / 2
    else:
        acct_multiplier = float(acct['multiplier'])
    acct_value = acct_equity * acct_multiplier
    return acct_value

def return_candles_json(symbol, period='1Day', num_bars=365):
    daily_bars_url_v1 = '{}/{}?symbols={}&limit={}'.format(BARS_URL, period, symbol, num_bars)
    daily_bars_url_v2 = 'https://data.alpaca.markets/v2/stocks/{}/bars?limit={}&timeframe={}'.format(symbol, num_bars, period)
    r = requests.get(daily_bars_url_v1, headers=HEADERS_PAPER)
    data = r.json()
    # df = pd.DataFrame(data)
    return data
