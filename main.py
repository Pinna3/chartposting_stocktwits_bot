import finnhub
import time

#Setup client
finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')

#get current realtime + 1yr ago as range inputs
current_time = int(time.time())
year_ago = int((time.time() - 31540000))

# Stock candles
res = finnhub_client.stock_candles('AAPL', 'D', year_ago, current_time)
print(res)

# print(time.localtime(current_time))
# print(time.localtime(year_ago))
