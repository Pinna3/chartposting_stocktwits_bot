from alpaca_environment_variables import*
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST
from time import time
from datetime import datetime
import pandas as pd

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_DATA_URL, api_version='v2')
# account = api.get_account()
# print(account.buying_power)
# orders = api.list_orders()
# print(api.cancel_order(orders[0].id))

start_time_epoch = time() - (365 * (31540000 / 365))
current_time_epoch = time()
start_time_datetime = datetime.fromtimestamp(start_time_epoch).strftime('%m-%d-%Y')
current_time_datetime = datetime.fromtimestamp(current_time_epoch).strftime('%m-%d-%Y')

# NY = 'America/New_York'
# start = pd.Timestamp(start_time_datetime, tz=NY).isoformat()
# print(api.get_barset(['AAPL'], 'day', start='03-27-2020').df)
print(api.get_bars("AAPL", TimeFrame.Hour, "2021-02-08", "2021-02-08", limit=10, adjustment='raw').df)

# print(dataframe)
# api.get_bars('AAPL', TimeFrame.Day, )
