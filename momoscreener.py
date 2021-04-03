import finnhub
import csv
from time import sleep
from candlestick import SecurityTradeData, LiteSecurityTradeData
from utility_func import bb_param_optomizer, make_pulled_csv_list_consumable
import json
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')
import operator
import os


class Securities:
    def __init__(self, csv_source):
        securities = make_pulled_csv_list_consumable(csv_source)
        candles = []
        for security in securities:
            candle_object = LiteSecurityTradeData(security)
            candles.append(candle_object)
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
        for index, candle_object in enumerate(self.candles):
            if len(candle_object.df) > time_markers[-1]:
                if candle_object.smoothness == 'TRUE':
                    pass_or_fail = []
                    #every 10 multiple = 2 trading weeks
                    for timebar in time_markers:
                        c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-timebar]
                        if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200):
                            pass_or_fail.append(True)
                        else:
                            pass_or_fail.append(False)

                    if False not in pass_or_fail:
                        bb_window, bb_std = bb_param_optomizer(candle_object, op_str, entry_frequency)
                        trending.append({'ticker': candle_object.ticker, 'sector': candle_object.sector,
                                        'mktcap': candle_object.mktcap, 'bb_window': bb_window,
                                        'bb_std': bb_std})#, 'peers': object.peers})
                        print(f'{candle_object.ticker}:{len(trending)}')
                    else:
                        print(index)
                else:
                    #finnhub backupsource
                    try:
                        backup_candle_object = SecurityTradeData(candle_object.ticker)
                        pass_or_fail = []
                        #every 10 multiple = 2 trading weeks
                        for timebar in time_markers:
                            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper = candle_object.df.iloc[-timebar]
                            if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200):
                                pass_or_fail.append(True)
                            else:
                                pass_or_fail.append(False)

                        if False not in pass_or_fail:
                            bb_window, bb_std = bb_param_optomizer(candle_object, op_str, entry_frequency)
                            trending.append({'ticker': candle_object.ticker, 'sector': candle_object.sector,
                                            'mktcap': candle_object.mktcap, 'bb_window': bb_window,
                                            'bb_std': bb_std})#, 'peers': object.peers})
                            print(f'{candle_object.ticker}:{len(trending)}')
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


# list = Securities('StockLists/Micro<$50M.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Micro', entry_frequency=6)
# list = Securities('StockLists/Small$50M-$300M.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Small', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Small', entry_frequency=6)
# list = Securities('StockLists/Medium$300M-$2B.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Medium', entry_frequency=6)
# list = Securities('StockLists/Large$2B-$10B.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Large', entry_frequency=6)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Large', entry_frequency=6)
list = Securities('StockLists/VeryLarge>$10B.csv')
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='VeryLarge', entry_frequency=6)
#
