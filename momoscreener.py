import finnhub
import csv
from time import sleep
from candlestick import SecurityTradeData
from utility_func import bb_param_optomizer
import json
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')
import operator


class Securities:
    def __init__(self, csv_source):
        securities = []
        # CSV Database- comprehensive list of optionable stocks obtain from barchart
        with open(csv_source, 'r') as infile:
            reader = csv.reader(infile)
            next(reader)  # skip the header line
            for row in reader:
                ticker = str(row[0])
                mktcap = row[5]
                securities.append([ticker, mktcap])
        # Setup finnhub client connection
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
        candles = []
        for security in securities:
            try:
                candle_object = SecurityTradeData(security[0], 365)
                #Setup client API connection
                finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
                try:
                    candle_object.industry = finnhub_client.company_profile2(symbol=security[0])['finnhubIndustry']
                except KeyError:
                    candle_object.industry = 'ETF'
                sleep(1)

                #peers data
                peers = finnhub_client.company_peers(security[0])
                sleep(1)
                hashable_peers = []
                for peer in peers:
                    hashable_peer = '$' + peer
                    hashable_peers.append(hashable_peer)
                candle_object.peers = hashable_peers[:3]
                candle_object.peers.append('$SPY')
                #Solves ETF lack of peers issue for publishing purposes
                if len(candle_object.peers) == 1:
                    candle_object.peers.append('$DIA')
                    candle_object.peers.append('$IWM')
                    candle_object.peers.append('$QQQ')
                candles.append(candle_object)
                print(f'{candle_object.ticker}: {len(candles)}/4578')

                #marketcap
                if int(security[1]) < 75000000:
                    mktcap = 'Micro'
                elif 75000000 < int(security[1]) < 300000000:
                    mktcap = 'Small'
                elif 300000000 < int(security[1]) < 1000000000:
                    mktcap = 'Medium'
                elif 1000000000 < int(security[1]) < 4000000000:
                    mktcap = 'Large'
                elif 4000000000 < int(security[1]):
                    mktcap = 'VeryLarge'
                candle_object.mktcap = mktcap
            except:
                continue
        self.candles = candles

    def __str__(self):
        return f'Securities(Length: {len(self.securities)})'

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_0w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/0w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (2w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_2w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/2w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (4w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_4w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/4w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (6w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_6w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/6w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (8w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_8w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = object.df.iloc[-60]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w) and \
                    op_func(sma98w, sma208w) and op_func(sma208w, sma508w) and op_func(sma508w, sma2008w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/8w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (10w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_10w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = object.df.iloc[-60]
                c10w, h10w, l10w, o10w, s10w, t10w, v10w, sma910w, sma2010w, sma5010w, sma20010w, lower, upper = object.df.iloc[-75]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w) and \
                    op_func(sma98w, sma208w) and op_func(sma208w, sma508w) and op_func(sma508w, sma2008w) and \
                    op_func(sma910w, sma2010w) and op_func(sma2010w, sma5010w) and op_func(sma5010w, sma20010w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/10w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (12w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_12w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = object.df.iloc[-60]
                c10w, h10w, l10w, o10w, s10w, t10w, v10w, sma910w, sma2010w, sma5010w, sma20010w, lower, upper = object.df.iloc[-75]
                c12w, h12w, l12w, o12w, s12w, t12w, v12w, sma912w, sma2012w, sma5012w, sma20012w, lower, upper = object.df.iloc[-90]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w) and \
                    op_func(sma98w, sma208w) and op_func(sma208w, sma508w) and op_func(sma508w, sma2008w) and \
                    op_func(sma910w, sma2010w) and op_func(sma2010w, sma5010w) and op_func(sma5010w, sma20010w) and \
                    op_func(sma912w, sma2012w) and op_func(sma2012w, sma5012w) and op_func(sma5012w, sma20012w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/12w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (14w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_14w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = object.df.iloc[-60]
                c10w, h10w, l10w, o10w, s10w, t10w, v10w, sma910w, sma2010w, sma5010w, sma20010w, lower, upper = object.df.iloc[-75]
                c12w, h12w, l12w, o12w, s12w, t12w, v12w, sma912w, sma2012w, sma5012w, sma20012w, lower, upper = object.df.iloc[-90]
                c14w, h14w, l14w, o14w, s14w, t14w, v14w, sma914w, sma2014w, sma5014w, sma20014w, lower, upper = object.df.iloc[-105]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w) and \
                    op_func(sma98w, sma208w) and op_func(sma208w, sma508w) and op_func(sma508w, sma2008w) and \
                    op_func(sma910w, sma2010w) and op_func(sma2010w, sma5010w) and op_func(sma5010w, sma20010w) and \
                    op_func(sma912w, sma2012w) and op_func(sma2012w, sma5012w) and op_func(sma5012w, sma20012w) and \
                    op_func(sma914w, sma2014w) and op_func(sma2014w, sma5014w) and op_func(sma5014w, sma20014w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/14w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (16w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_16w(self, op_str, mktcap_group):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = object.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = object.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = object.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = object.df.iloc[-60]
                c10w, h10w, l10w, o10w, s10w, t10w, v10w, sma910w, sma2010w, sma5010w, sma20010w, lower, upper = object.df.iloc[-75]
                c12w, h12w, l12w, o12w, s12w, t12w, v12w, sma912w, sma2012w, sma5012w, sma20012w, lower, upper = object.df.iloc[-90]
                c14w, h14w, l14w, o14w, s14w, t14w, v14w, sma914w, sma2014w, sma5014w, sma20014w, lower, upper = object.df.iloc[-105]
                c16w, h16w, l16w, o16w, s16w, t16w, v16w, sma916w, sma2016w, sma5016w, sma20016w, lower, upper = object.df.iloc[-120]
                if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200) and \
                    op_func(sma92w, sma202w) and op_func(sma202w, sma502w) and op_func(sma502w, sma2002w) and \
                    op_func(sma94w, sma204w) and op_func(sma204w, sma504w) and op_func(sma504w, sma2004w) and \
                    op_func(sma96w, sma206w) and op_func(sma206w, sma506w) and op_func(sma506w, sma2006w) and \
                    op_func(sma98w, sma208w) and op_func(sma208w, sma508w) and op_func(sma508w, sma2008w) and \
                    op_func(sma910w, sma2010w) and op_func(sma2010w, sma5010w) and op_func(sma5010w, sma20010w) and \
                    op_func(sma912w, sma2012w) and op_func(sma2012w, sma5012w) and op_func(sma5012w, sma20012w) and \
                    op_func(sma914w, sma2014w) and op_func(sma2014w, sma5014w) and op_func(sma5014w, sma20014w) and \
                    op_func(sma916w, sma2016w) and op_func(sma2016w, sma5016w) and op_func(sma5016w, sma20016w):
                    bb_window, bb_std = bb_param_optomizer(object, op_str)
                    trending.append({'ticker': object.ticker, 'industry': object.industry,
                                    'mktcap': object.mktcap, 'bb_window': bb_window,
                                    'bb_std': bb_std, 'peers': object.peers})
                    print(f'{object.ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/16w-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)

# # Filter full list for volume and market cap
# class FilteredOptionable(Securities):
#     def __init__(self, csv_source, min_mktcap, min_volume):
#         securities = []
#         # CSV Database- comprehensive list of optionable stocks obtain from barchart
#         with open(csv_source, 'r') as infile:
#             reader = csv.reader(infile)
#             next(reader)  # skip the header line
#             for row in reader:
#                 ticker = str(row[0])
#                 if row[3] != 'N/A' and row[3] != '':
#                     volume = float(row[3])
#                 if volume > min_volume:
#                     securities.append(ticker)
#         self.securities = securities

list = Securities('StockLists/MicroStocks$1M-$75M.csv')
list.trend_0w('>', 'Micro')
list.trend_2w('>', 'Micro')
list.trend_4w('>', 'Micro')
list.trend_6w('>', 'Micro')
list.trend_8w('>', 'Micro')
list.trend_10w('>', 'Micro')
list.trend_12w('>', 'Micro')
list.trend_14w('>', 'Micro')
list.trend_16w('>', 'Micro')
list.trend_0w('<', 'Micro')
list.trend_2w('<', 'Micro')
list.trend_4w('<', 'Micro')
list.trend_6w('<', 'Micro')
list.trend_8w('<', 'Micro')
list.trend_10w('<', 'Micro')
list.trend_12w('<', 'Micro')
list.trend_14w('<', 'Micro')
list.trend_16w('<', 'Micro')

list = Securities('StockLists/SmallStocks$75M-$300M.csv')
list.trend_0w('>', 'Small')
list.trend_2w('>', 'Small')
list.trend_4w('>', 'Small')
list.trend_6w('>', 'Small')
list.trend_8w('>', 'Small')
list.trend_10w('>', 'Small')
list.trend_12w('>', 'Small')
list.trend_14w('>', 'Small')
list.trend_16w('>', 'Small')
list.trend_0w('<', 'Small')
list.trend_2w('<', 'Small')
list.trend_4w('<', 'Small')
list.trend_6w('<', 'Small')
list.trend_8w('<', 'Small')
list.trend_10w('<', 'Small')
list.trend_12w('<', 'Small')
list.trend_14w('<', 'Small')
list.trend_16w('<', 'Small')

list = Securities('StockLists/MediumStocks$300M-$1B.csv')
list.trend_0w('>', 'Medium')
list.trend_2w('>', 'Medium')
list.trend_4w('>', 'Medium')
list.trend_6w('>', 'Medium')
list.trend_8w('>', 'Medium')
list.trend_10w('>', 'Medium')
list.trend_12w('>', 'Medium')
list.trend_14w('>', 'Medium')
list.trend_16w('>', 'Medium')
list.trend_0w('<', 'Medium')
list.trend_2w('<', 'Medium')
list.trend_4w('<', 'Medium')
list.trend_6w('<', 'Medium')
list.trend_8w('<', 'Medium')
list.trend_10w('<', 'Medium')
list.trend_12w('<', 'Medium')
list.trend_14w('<', 'Medium')
list.trend_16w('<', 'Medium')

list = Securities('StockLists/LargeStocks$1B-$4B.csv')
list.trend_0w('>', 'Large')
list.trend_2w('>', 'Large')
list.trend_4w('>', 'Large')
list.trend_6w('>', 'Large')
list.trend_8w('>', 'Large')
list.trend_10w('>', 'Large')
list.trend_12w('>', 'Large')
list.trend_14w('>', 'Large')
list.trend_16w('>', 'Large')
list.trend_0w('<', 'Large')
list.trend_2w('<', 'Large')
list.trend_4w('<', 'Large')
list.trend_6w('<', 'Large')
list.trend_8w('<', 'Large')
list.trend_10w('<', 'Large')
list.trend_12w('<', 'Large')
list.trend_14w('<', 'Large')
list.trend_16w('<', 'Large')

list = Securities('StockLists/VeryLargeStocks$4B+.csv')
list.trend_0w('>', 'VeryLarge')
list.trend_2w('>', 'VeryLarge')
list.trend_4w('>', 'VeryLarge')
list.trend_6w('>', 'VeryLarge')
list.trend_8w('>', 'VeryLarge')
list.trend_10w('>', 'VeryLarge')
list.trend_12w('>', 'VeryLarge')
list.trend_14w('>', 'VeryLarge')
list.trend_16w('>', 'VeryLarge')
list.trend_0w('<', 'VeryLarge')
list.trend_2w('<', 'VeryLarge')
list.trend_4w('<', 'VeryLarge')
list.trend_6w('<', 'VeryLarge')
list.trend_8w('<', 'VeryLarge')
list.trend_10w('<', 'VeryLarge')
list.trend_12w('<', 'VeryLarge')
list.trend_14w('<', 'VeryLarge')
list.trend_16w('<', 'VeryLarge')
