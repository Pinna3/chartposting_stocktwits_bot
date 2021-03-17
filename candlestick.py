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

        #### EXPERIMENTAL (ADJUST WINDOW AND MULTIPLE) (NEEDS TWEAKING)
        bollinger_reference_lower = df.l.rolling(window=10, min_periods=1).mean()
        bollinger_reference_upper = df.h.rolling(window=10, min_periods=1).mean()
        sigma_lower = df.l.rolling(window=10, min_periods=1).std()
        sigma_upper = df.h.rolling(window=10, min_periods=1).std()
        df['lower'] = bollinger_reference_lower - 1.1 * sigma_lower
        df['upper'] = bollinger_reference_upper + 1.1 * sigma_upper

        self.df = df

    def __str__(self):
        c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = self.df.iloc[-1]
        return f'DailyCandleDataRT({self.ticker}-{self.num_days}d: Close/Current:{c}, ' +\
               f'9SMA:{sma9}, 20SMA:{sma20}, 50SMA:{sma50}, 200SMA:{sma200})'

# #This is how I will screen for trending stocks in realtime throughout the day
# c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = DailyCandleDataRT('GOOGL', 365).df.iloc[-1]
# print(c > sma20 > sma50 > sma200)

    def chart(self, days):
        #Using index for x-axis until I can figure out how to use date without empties
        trace_bar = {'x': self.df.index, 'open': self.df['o'][-days:], 'close': self.df['c'][-days:], 'high': self.df['h'][-days:],
            'low': self.df['l'][-days:], 'type': 'candlestick', 'name': self.ticker, 'showlegend': True}
        trace_9sma = {'x': self.df.index, 'y': self.df['sma9'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '9 SMA'}
        trace_20sma = {'x': self.df.index, 'y': self.df['sma20'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '20 SMA'}
        trace_50sma = {'x': self.df.index, 'y': self.df['sma50'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '50 SMA'}
        trace_200sma = {'x': self.df.index, 'y': self.df['sma200'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '200 SMA'}

        ###EXPERIMENTAL
        trace_lower = {'x': self.df.index, 'y': self.df['lower'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'LowerBB'}
        trace_upper = {'x': self.df.index, 'y': self.df['upper'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'UpperBB'}

        data = [trace_bar, trace_9sma, trace_20sma, trace_50sma, trace_200sma, trace_lower, trace_upper]

        layout = go.Layout({'title': {'text': f'{self.ticker} Moving Averages',
                'font': {'size': 15}}})

        fig = go.Figure(data=data, layout=layout)
        # fig.write_html("Microsoft(MSFT) Moving Averages.html")

        return fig.show()


### ['AAL', 'AB', 'ABB', 'ABR']
# DailyCandleDataRT('AB', 365).chart(365)
