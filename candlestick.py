import pandas
import plotly.graph_objs as go
import finnhub, time, operator
import pandas as pd
import os
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')
hours_minutes_now = datetime.now().strftime('%H:%M')
from alpaca import return_candles_json

#Database Object with candlestick data and moving average data (for now)
#timeseries data should cover the longest moving average period 200 + the # of days of longest trend test
class SecurityTradeData:
    # @memoize
    def __init__(self, ticker, period_len='day', num_of_periods=281, atr_rolling_window=14):
        #basics
        self.ticker = ticker
        self.period = period_len
        self.num_of_periods = num_of_periods
        self.start_time = int((time.time() - (num_of_periods * (31540000 / 365))))
        self.current_time = int(time.time())

        #sector and peers data added while scanning
        self.sector = None
        self.peers = None
        self.mktcap = None
        self.smoothness = None

        #candlestick data (Alpaca API Primary, Finnhub backup)
        # try:
        smoothness_test = True
        data = None
        while data is None:
            try:
                data = return_candles_json(ticker, period_len, num_bars=num_of_periods)
                time.sleep(.7)
            except:
                continue
        for index, ohlc in enumerate(data[ticker][:-1]):
            if abs(float(ohlc['c']) - float(data[ticker][index+1]['o'])) > (float(ohlc['c']) * .5):
                smoothness_test = False
        df = pd.DataFrame(data[ticker])
        del df['t']
        time.sleep(.3)
        # except KeyError:
            # smoothness_test = False

        #finnhub backup for split gaps (set for unlimited pings right now... counter is prob more practical)
        if smoothness_test == False:
            finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
            data = None
            while data is None:
                try:
                    data = finnhub_client.stock_candles(ticker, 'D', self.start_time, self.current_time)
                    time.sleep(1.1)
                except:
                    continue
            del data['s']
            del data['t']
            df = pd.DataFrame(data)
            time.sleep(.7)

        df['sma9'] = round(df.c.rolling(window=9, min_periods=9).mean(), 2)
        df['sma20'] = round(df.c.rolling(window=20, min_periods=20).mean(), 2)
        df['sma50'] = round(df.c.rolling(window=50, min_periods=50).mean(), 2)
        df['sma200'] = round(df.c.rolling(window=200, min_periods=200).mean(), 2)
        #### standard  2 and 20 bollinger data
        bollinger_reference_lower = df.l.rolling(window=20, min_periods=20).mean()
        bollinger_reference_upper = df.h.rolling(window=20, min_periods=20).mean()
        sigma_lower = df.l.rolling(window=20, min_periods=20).std()
        sigma_upper = df.h.rolling(window=20, min_periods=20).std()
        df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
        df['upper'] = bollinger_reference_upper + (2 * sigma_upper)
        #### average true range pandas_atr_calculation
        df['atr'] = pandas_atr_calculation(df, atr_rolling_window)
        # #Play with shifting method to optimize ATR mulitple for traling stops
        # df['top_atr'] = df['h'].shift(periods=-2) + (1 * df['atr'])
        # df['bottom_atr'] = df['l'].shift(periods=-2) - (1 * df['atr'])
        self.df = df

    def __str__(self):
        c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = self.df.iloc[-1]
        return f'SecurityTradeData({self.ticker}-{self.sector}-{self.mktcap})'#: Close/Current:{c}, ' +\
               # f'9SMA:{sma9}, 20SMA:{sma20}, 50SMA:{sma50}, 200SMA:{sma200})'

    def custom_bollingers(self, bollinger_rolling_window, bollinger_std):
        try:
            bollinger_reference_lower = self.df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
            bollinger_reference_upper = self.df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).mean()
            sigma_lower = self.df.l.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
            sigma_upper = self.df.h.rolling(window=bollinger_rolling_window, min_periods=bollinger_rolling_window).std()
            self.df['lower'] = bollinger_reference_lower - (bollinger_std * sigma_lower)
            self.df['upper'] = bollinger_reference_upper + (bollinger_std * sigma_upper)
        except ValueError:
            bollinger_reference_lower = self.df.l.rolling(window=20, min_periods=20).mean()
            bollinger_reference_upper = self.df.h.rolling(window=20, min_periods=20).mean()
            sigma_lower = self.df.l.rolling(window=20, min_periods=20).std()
            sigma_upper = self.df.h.rolling(window=20, min_periods=20).std()
            self.df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
            self.df['upper'] = bollinger_reference_upper + (2 * sigma_upper)

    def sma200_double_agent_activate(self, rolling_window):
        self.df['sma200'] = round(self.df.c.rolling(window=rolling_window, min_periods=rolling_window).mean(), 2)

    #destination options: 'browser', or filepaths 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def chart(self, days, destination='browser'):
        ###CANDLESTICK AND MOVING AVERAGE DATA
        trace_bar = {'x': self.df.index, 'open': self.df['o'][-days:], 'close': self.df['c'][-days:], 'high': self.df['h'][-days:],
            'low': self.df['l'][-days:], 'type': 'candlestick', 'name': self.ticker, 'showlegend': True}
        trace_9sma = {'x': self.df.index, 'y': self.df['sma9'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '9SMA'}
        trace_20sma = {'x': self.df.index, 'y': self.df['sma20'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '20SMA'}
        trace_50sma = {'x': self.df.index, 'y': self.df['sma50'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '50SMA'}
        trace_200sma = {'x': self.df.index, 'y': self.df['sma200'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'blue'}, 'name': '200SMA'}

        ###BOLLINGERS
        trace_lower = {'x': self.df.index, 'y': self.df['lower'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'LowerBB'}
        trace_upper = {'x': self.df.index, 'y': self.df['upper'][-days:], 'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': 'red'}, 'name': 'UpperBB'}

        # ###ATR (For help with ATR optimization)
        # trace_atr_lower = {'x': self.df.index, 'y': self.df['bottom_atr'][-days:], 'type': 'scatter', 'mode': 'lines',
        #     'line': {'width': 1, 'color': 'blue'}, 'name': 'B-ATR'}
        # trace_atr_upper = {'x': self.df.index, 'y': self.df['top_atr'][-days:], 'type': 'scatter', 'mode': 'lines',
        #     'line': {'width': 1, 'color': 'blue'}, 'name': 'T-ATR'}

        #plot data
        data = [trace_bar, trace_9sma, trace_20sma, trace_50sma, trace_200sma, trace_lower, trace_upper]
        # data2 = [trace_bar, trace_atr_lower, trace_atr_upper]
        #chart aesthetic
        layout = go.Layout(#'title': {'text': f'{self.ticker} {days}D Daily Chart', 'yanchor': 1.0},
                            {'font': {'size': 12}, 'width': 1200, 'height': 675,
                            'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
                            'xaxis': {'rangeslider': {'visible': False}},
                            'legend': {'yanchor': 'top', 'y': 1.0, 'xanchor': 'left',
                                       'x': 0, 'orientation': 'h', 'font':{'size': 12}},
                            'yaxis': {'side': 'right'}})

        #chart init
        fig = go.Figure(data=data, layout=layout)

        if destination == 'browser':
            return fig.show()

        else:
            if not os.path.exists(f'{destination}Stocks/Charts/{today_date}'):
                os.mkdir(f'{destination}Stocks/Charts/{today_date}')
            fig.write_image(f'{destination}Stocks/Charts/{today_date}/{self.ticker}.png')


    #counts number of bollinger interceptions (i.e. entries for use in optimization)
    #use op_str '>' for uptrend and op_str '<' for downtrend
    ###MAKE FASTER
    #Remember entry count is limited by average time variable, eliminates repeats (consider removing or implementing average variable)
    def entry_counter_bollingers_WITH_average(self, op_str, timebar):
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
        #ignoring other sma9 >/< sma20 >/< sma50 >/< sma200 condtion for now (HYPOTHESIS: UNNECESSARY IN CURRENT OPERATING CONTEXT)
        for index, row in dataframe.iloc[-timebar:].iterrows():
            if op_reversed_func(row[h_or_l], row[bollinger]) and op_func(row['sma9'], row['sma20']) and op_func(row['sma20'], row['sma50']) and op_func(row['sma50'], row['sma200']):
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

    def entry_counter_bollingers_WITHOUT_average(self, op_str, timebar):
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
        #ignoring other sma9 >/< sma20 >/< sma50 >/< sma200 condtion for now (HYPOTHESIS: UNNECESSARY IN CURRENT OPERATING CONTEXT)
        for index, row in dataframe.iloc[-timebar:].iterrows():
            if op_reversed_func(row[h_or_l], row[bollinger]):# and op_func(row['sma9'], row['sma20']) and op_func(row['sma20'], row['sma50']) and op_func(row['sma50'], row['sma200']):
                entries.append(index)
        total = len(entries)
        return total

    #Remember entry count is limited by average time variable, eliminates repeats (consider removing or implementing average variable)
    def entry_counter_200sma_double_agent_WITH_average(self, op_str):
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
        #ignoring other sma9 >/< sma20 >/< sma50 >/< sma200 condtion for now (HYPOTHESIS: UNNECESSARY IN CURRENT OPERATING CONTEXT)
        for index, row in dataframe.iterrows():
            if op_reversed_func(row[h_or_l], row['sma200']):# and op_func(row['sma9'], row['sma20']) and op_func(row['sma20'], row['sma50']):
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

    def entry_counter_200sma_double_agent_WITHOUT_average(self, op_str, timebar):
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
        #ignoring other sma9 >/< sma20 >/< sma50 >/< sma200 condtion for now (HYPOTHESIS: UNNECESSARY IN CURRENT OPERATING CONTEXT)
        for index, row in dataframe.iloc[-timebar:].iterrows():
            if op_reversed_func(row[h_or_l], row['sma200']):# and op_func(row['sma9'], row['sma20']) and op_func(row['sma20'], row['sma50']):
                entries.append(index)
        total = len(entries)
        return total


#SecurityTradeData object when all attributes are provided as inputs
class LiteSecurityTradeData(SecurityTradeData):
    def __init__(self, consumable_item, period_len='day', atr_rolling_window=14):
        #basics
        self.ticker = consumable_item[0]
        self.period = period_len
        #sector and peers data added while scanning
        self.sector = consumable_item[2]
        self.peers = consumable_item[4]
        self.mktcap = consumable_item[1]
        self.smoothness = consumable_item[3]
        self.sma200_double_agent = consumable_item[5]
        df = consumable_item[6]
        df['sma9'] = round(df.c.rolling(window=9, min_periods=9).mean(), 2)
        df['sma20'] = round(df.c.rolling(window=20, min_periods=20).mean(), 2)
        df['sma50'] = round(df.c.rolling(window=50, min_periods=50).mean(), 2)
        df['sma200'] = round(df.c.rolling(window=200, min_periods=200).mean(), 2)
        #### standard  2 and 20 bollinger data
        bollinger_reference_lower = df.l.rolling(window=20, min_periods=20).mean()
        bollinger_reference_upper = df.h.rolling(window=20, min_periods=20).mean()
        sigma_lower = df.l.rolling(window=20, min_periods=20).std()
        sigma_upper = df.h.rolling(window=20, min_periods=20).std()
        df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
        df['upper'] = bollinger_reference_upper + (2 * sigma_upper)
        #ATR w/ Wilders EMA
        df['atr'] = pandas_atr_calculation(df, atr_rolling_window)
        self.df = df

def pandas_atr_calculation(df, window=14):
    def wilder_ema(results, window):
        return results.ewm(alpha=1/window, adjust=False).mean()

    df = df.copy()
    high = df.h
    low = df.l
    close = df.c
    df['tr0'] = abs(high - low)
    df['tr1'] = abs(high - close.shift())
    df['tr2'] = abs(low - close.shift())
    true_range = df[['tr0', 'tr1', 'tr2']].max(axis=1)
    return wilder_ema(true_range, window)

# test = SecurityTradeData('LB', atr_rolling_window=14)
# test.custom_bollingers(3, .1)
# test.chart(281)
# print(test.df)
# print(test.entry_counter_bollingers_WITHOUT_average('>'))
# print(test.df.iloc[-1])
