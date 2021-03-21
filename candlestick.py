import pandas as pd
import plotly.graph_objs as go
import finnhub
import time
import operator

#Database Object with candlestick data and moving average data (for now)
class DailyCandleDataRT:
    def __init__(self, ticker, num_days, bollinger_rolling_window, bollinger_std):
        self.ticker = ticker
        self.num_days = num_days
        self.start_time = int((time.time() - (num_days * (31540000 / 365))))
        self.current_time = int(time.time())

        #Setup client
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        #candlestick data
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

        #### bollinger data (needs tweaking)
        bollinger_reference_lower = df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
        bollinger_reference_upper = df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
        sigma_lower = df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
        sigma_upper = df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
        df['lower'] = bollinger_reference_lower - (bollinger_std * sigma_lower)
        df['upper'] = bollinger_reference_upper + (bollinger_std * sigma_upper)

        self.df = df

    def __str__(self):
        c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = self.df.iloc[-1]
        return f'DailyCandleDataRT({self.ticker}-{self.num_days}d: Close/Current:{c}, ' +\
               f'9SMA:{sma9}, 20SMA:{sma20}, 50SMA:{sma50}, 200SMA:{sma200})'

# #This is how I will screen for trending stocks in realtime throughout the day
# c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = DailyCandleDataRT('GOOGL', 365).df.iloc[-1]
# print(c > sma20 > sma50 > sma200)

    def chart(self, days):
        ###CANDLESTICK DATA AND MOVING AVERAGE DATA
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

        ###BOLLINGERS (NEEDS TWEAKING)
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

####use op_str '>' for uptrend and op_str '<' for downtrend
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
        print(f'Total: {entries}')
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
        print(f'Sum: {sum}')
        try:
            average = total / sum
        except ZeroDivisionError:
            print(f'Average Entry Length: {0}')
            return [0, 0]
        print(f'Average Entry Length: {average}')
        return [len(entries), average]


# test = DailyCandleDataRT('CLNY', 365, 3, 1)
# test.chart(120)
# print(test.df)
# print(test.entry_counter('>'))




# for rolling_window in range(50):
#     time.sleep(1)
#     print(rolling_window)
#     DailyCandleDataRT('CLNY', 365, rolling_window, 1).entry_counter('>')

# for std in [.2, .4, .6, .8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]:
#     print(std)
#     print(DailyCandleDataRT('CLNY', 365, 3, std).entry_counter('>'))
