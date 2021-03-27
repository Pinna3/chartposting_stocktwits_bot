import pandas as pd
import plotly.graph_objs as go
import finnhub
import time
import operator
# from utility_func import memoize

#Database Object with candlestick data and moving average data (for now)
class SecurityTradeData:
    # @memoize
    def __init__(self, ticker, num_days):
        #basics
        self.ticker = ticker
        self.num_days = num_days
        self.start_time = int((time.time() - (num_days * (31540000 / 365))))
        self.current_time = int(time.time())

        #Setup client API connection
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        #industry and peers data added while scanning
        self.industry = None
        self.peers = None
        self.mktcap = None

        #candlestick data
        data = finnhub_client.stock_candles(ticker, 'D', self.start_time, self.current_time)
        time.sleep(1)
        df = pd.DataFrame(data)
        sma9 = round(df.c.rolling(window=9, min_periods=1).mean(), 2)
        sma20 = round(df.c.rolling(window=20, min_periods=1).mean(), 2)
        sma50 = round(df.c.rolling(window=50, min_periods=1).mean(), 2)
        sma200 = round(df.c.rolling(window=200, min_periods=1).mean(), 2)
        df['sma9'] = sma9
        df['sma20'] = sma20
        df['sma50'] = sma50
        df['sma200'] = sma200
        #### standard  2 and 20 bollinger data
        bollinger_reference_lower = df.l.rolling(window=20, min_periods=20).mean()
        bollinger_reference_upper = df.h.rolling(window=20, min_periods=20).mean()
        sigma_lower = df.l.rolling(window=20, min_periods=20).std()
        sigma_upper = df.h.rolling(window=20, min_periods=20).std()
        df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
        df['upper'] = bollinger_reference_upper + (2 * sigma_upper)
        self.df = df

    def __str__(self):
        c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = self.df.iloc[-1]
        return f'SecurityTradeData({self.ticker}-{self.num_days}d: Close/Current:{c}, ' +\
               f'9SMA:{sma9}, 20SMA:{sma20}, 50SMA:{sma50}, 200SMA:{sma200})'

    def custom_bollingers(self, bollinger_rolling_window, bollinger_std):
        bollinger_reference_lower = self.df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
        bollinger_reference_upper = self.df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
        sigma_lower = self.df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
        sigma_upper = self.df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
        self.df['lower'] = bollinger_reference_lower - (bollinger_std * sigma_lower)
        self.df['upper'] = bollinger_reference_upper + (bollinger_std * sigma_upper)

    def chart(self, days):
        ###CANDLESTICK AND MOVING AVERAGE DATA
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

        ###BOLLINGERS
        trace_lower = {'x': self.df.index, 'y': self.df['lower'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'LowerBB'}
        trace_upper = {'x': self.df.index, 'y': self.df['upper'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'UpperBB'}

        #plot data
        data = [trace_bar, trace_9sma, trace_20sma, trace_50sma, trace_200sma, trace_lower, trace_upper]

        #chart aesthetic
        layout = go.Layout({'title': {'text': f'{self.ticker} Moving Averages',
                'font': {'size': 15}}})

        #chart init
        fig = go.Figure(data=data, layout=layout)
        # fig.write_html("Microsoft(MSFT) Moving Averages.html")

        #show chart
        return fig.show()

    #counts number of bollinger interceptions (i.e. entries for use in optimization)
    #use op_str '>' for uptrend and op_str '<' for downtrend
    def entry_counter(self, op_str):
        dataframe = self.df
        entries = []
        repeats = []
        groupings = set()

        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        ops_reversed = {">": operator.lt, "<": operator.gt}
        op_reversed_func = ops_reversed[op_str]
        if op_str == '>':
            h_or_l = 'l'
        if op_str == '<':
            h_or_l = 'h'
        if op_str == '>':
            bollinger = 'lower'
        if op_str == '<':
            bollinger = 'upper'

        for index, row in dataframe.iterrows():
            if op_reversed_func(row[h_or_l], row[bollinger]) and op_func(row['sma9'], row['sma20']) \
                and op_func(row['sma20'], row['sma50']) and op_func(row['sma50'], row['sma200']):
                entries.append(index)
        total = len(entries)
        i = 0
        while i < len(entries):
            try:
                if entries[i] - entries[i + 1] == -1:
                    entries.remove(entries[i])
                    repeats.append(i)
                    groupings.add(i)
                    i -= 1
                else:
                    i += 1
            except IndexError:
                break
        sum = 0
        for grouping in groupings:
            sum += repeats.count(grouping)
        sum += len(entries) - len(repeats)
        try:
            average = total / sum
        except ZeroDivisionError:
            return [0, 0]
        return [sum, average]

# print(SecurityTradeData('AAPL', 15).df)
