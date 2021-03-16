import pandas as pd
import plotly.graph_objs as go
import finnhub
import time

#Setup client
finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')

#Daily candle pandas dataframe
def daily_candle_df_rt(ticker, num_days):
    current_time = int(time.time())
    start_time = int((time.time() - num_days * (31540000 / 365)))

    data = finnhub_client.stock_candles(ticker, 'D', start_time, current_time)
    df = pd.core.frame.DataFrame(data)
    sma9 = round(df.c.rolling(window=9, min_periods=1).mean(), 2)
    sma20 = round(df.c.rolling(window=20, min_periods=1).mean(), 2)
    sma50 = round(df.c.rolling(window=50, min_periods=1).mean(), 2)
    sma200 = round(df.c.rolling(window=200, min_periods=1).mean(), 2)
    df['sma9'] = sma9
    df['sma20'] = sma20
    df['sma50'] = sma50
    df['sma200'] = sma200
    return df
print(daily_candle_df_rt('TSLA', 365))



# #bar trace
# trace_bar = {
#     'x': df_aapl.t,
#     'open': df_aapl.o,
#     'close': df_aapl.c,
#     'high': df_aapl.h,
#     'low': df_aapl.l,
#     'type': 'candlestick',
#     'name': 'AAPL',
#     'showlegend': True
# }
#
# data = [trace_bar]
# layout = go.Layout({
#     'title': {
#         'text': 'Apple (AAPL) Moving Averages',
#         'font': {
#             'size': 15
#         }
#     }
# })
#
# fig = go.Figure(data=data, layout=layout)
# # fig.write_html("Microsoft(MSFT) Moving Averages.html")
# fig.show()

# #9sma data (9 simple moving average)
# sma9 = df_aapl.c.rolling(window=9, min_periods=1).mean()
# # print(sma9)
#
# #9sma trace (9 simple moving average)
# trace_9sma = {
#     'x': df_aapl.index,
#     'y': sma9,
#     'type': 'scatter',
#     'mode': 'lines',
#     'line': {
#         'width': 1,
#         'color': 'blue'
#             },
#     'name': '9 Simple Moving Average'
# }
#
# #20sma data (20 simple moving average)
# sma20 = df_aapl.c.rolling(window=20, min_periods=1).mean()
# # print(sma20)
#
# #50sma data (50 simple moving average)
# sma50 = df_aapl.c.rolling(window=50, min_periods=1).mean()
# # print(sma50)
#
# #100sma data (100 simple moving average)
# sma100 = df_aapl.c.rolling(window=100, min_periods=1).mean()
# # print(sma100)
#
# #200sma data (200 simple moving average)
# sma200 = df_aapl.c.rolling(window=200, min_periods=1).mean()
# # print(sma200)
