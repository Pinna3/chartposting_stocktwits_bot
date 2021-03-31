import finnhub
import csv
from time import sleep
from candlestick import SecurityTradeData
from utility_func import bb_param_optomizer
import json
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')
import operator
import os


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
                print(f'{candle_object.ticker}: {len(candles)}/{len(securities)}')

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

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (16w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_9SMA_20SMA_50SMA_200SMA(self, *time_markers, op_str='>', mktcap_group='VeryLarge', entry_frequency=12):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        for index, object in enumerate(self.candles):
            try:
                pass_or_fail = []
                #every 10 multiple = 2 trading weeks
                for timebar in time_markers:
                    c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper = object.df.iloc[-timebar]
                    if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200):
                        pass_or_fail.append(True)
                    else:
                        pass_or_fail.append(False)
                if False not in pass_or_fail:
                    bb_window, bb_std = bb_param_optomizer(object, op_str, entry_frequency)
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

        if not os.path.exists(f'{mktcap_group}Stocks/Watchlists/{today_date}'):
            os.mkdir(f'{mktcap_group}Stocks/Watchlists/{today_date}')
        with open(f'{mktcap_group}Stocks/Watchlists/{today_date}/{time_markers[-1:]}D-{entry_frequency}E-{trend}trend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)


list = Securities('StockLists/MicroStocks$1M-$75M.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Micro', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Micro', entry_frequency=4)
list = Securities('StockLists/SmallStocks$75M-$300M.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Small', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Small', entry_frequency=4)
list = Securities('StockLists/MediumStocks$300M-$1B.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Medium', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Medium', entry_frequency=4)
list = Securities('StockLists/LargeStocks$1B-$4B.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Large', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Large', entry_frequency=4)
list = Securities('StockLists/VeryLargeStocks$4B+.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='VeryLarge', entry_frequency=4)
#
