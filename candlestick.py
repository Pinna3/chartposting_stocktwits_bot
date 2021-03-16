import pandas as pd
import plotly.graph_objs as go
import finnhub
import time

#Database Object with candlestick data and moving average data (for now)
class DailyCandleDataRT:
    def __init__(self, ticker, num_days):
        self.ticker = ticker
        self.num_days = num_days
        self.start_time = int((time.time() - (num_days * (31540000 / 365))))
        self.current_time = int(time.time())

        #Setup client
        finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')
        #dataframe data
        data = finnhub_client.stock_candles(ticker, 'D', self.start_time, self.current_time)
        df = pd.DataFrame(data)
        sma9 = round(df.c.rolling(window=9, min_periods=1).mean(), 2)
        sma20 = round(df.c.rolling(window=20, min_periods=1).mean(), 2)
        sma50 = round(df.c.rolling(window=50, min_periods=1).mean(), 2)
        sma200 = round(df.c.rolling(window=200, min_periods=1).mean(), 2)
        df['sma9'] = sma9
        df['sma20'] = sma20
        df['sma50'] = sma50
        df['sma200'] = sma200
        self.df = df

    def __str__(self):
        c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = self.df.iloc[-1]
        return f'DailyCandleDataRT({self.ticker}-{self.num_days}d: Close/Current:{c}, ' +\
               f'9SMA:{sma9}, 20SMA:{sma20}, 50SMA:{sma50}, 200SMA:{sma200})'


#This is how I will screen for trending stocks in realtime throughout the day
c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = DailyCandleDataRT('GOOGL', 365).df.iloc[-1]
print(c > sma20 > sma50 > sma200)






##########################Set this up as a method of the database object
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
