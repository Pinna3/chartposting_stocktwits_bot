import finnhub
import csv
from time import sleep
from candlestick import SecurityTradeData, LiteSecurityTradeData
from utility_func import bb_param_optomizer_WITH_average, bb_param_optomizer_WITHOUT_average, sm200doubleagent_window_optomizer_WITHOUT_average, make_pulled_csv_list_consumable
import json
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')
import operator
import os


class Securities:
    def __init__(self, csv_source):
        securities = make_pulled_csv_list_consumable(csv_source)
        candles = []
        backup_candles = []
        for index, security in enumerate(securities):
            if security[3] == 'TRUE':
                candle_object = LiteSecurityTradeData(security)
                print(f'{index}/{len(securities)} - {security[0]}')
                candles.append(candle_object)
            elif security[3] == 'FALSE':
                backup_candle_object = None
                while backup_candle_object is None:
                    try:
                        backup_candle_object = SecurityTradeData(security[0])
                        backup_candle_object.sector = security[2]
                        backup_candle_object.peers = security[4]
                        backup_candle_object.mktcap = security[1]
                        print(f'{index}/{len(securities)} - {security[0]} - FINNHUB BACKUP')
                        backup_candles.append(backup_candle_object)
                    except:
                        continue
        self.candles = candles
        self.backup_candles = backup_candles

    def __str__(self):
        return f'Securities(Length: {len(self.securities)})'

    # 9SMA >/< 20SMA >/< 50SMA >/< 200SMA (16w ago - current) [op_str = '>' for uptrend]
    #mktcap_group = 'Micro', 'Small', 'Medium', 'Large', 'VeryLarge'
    def trend_9SMA_20SMA_50SMA_200SMA(self, *time_markers, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1.25):#, ror_prioritization_factor=2.25):
        #up/down trendtrend toggle
        ops = {"<": operator.lt, ">": operator.gt}
        op_func = ops[op_str]
        #loop through securities and filter for up/down trends
        trending = []
        def main(candle_list):
            for index, candle_object in enumerate(candle_list):
                # try:
                    if len(candle_object.df) > (time_markers[-1] + 200):
                        pass_or_fail = []
                        #every 10 multiple = 2 trading weeks
                        for timebar in time_markers:
                            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle_object.df.iloc[-timebar]
                            if op_func(sma9, sma20) and op_func(sma20, sma50) and op_func(sma50, sma200):
                                pass_or_fail.append(True)
                            else:
                                pass_or_fail.append(False)
                        if False not in pass_or_fail:
                            c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle_object.df.iloc[-timebar]
                            clast, hlast, llast, olast, vlast, sma9last, sma20last, sma50last, sma200last, lowerlast, upperlast, atrlast = candle_object.df.iloc[-1]
                            if op_str == '>':
                                ror = round((((clast - o) / o) * 100), 2)
                            elif op_str == '<':
                                ror = round(-(((clast - o) / o) * 100), 2)
                            if ror > 0:
                                entry_frequency = int(round((ror_prioritization_factor * ror) + 1, 0))
                            else:
                                entry_frequency = int(ror_prioritization_factor)
                            sma200_double_agent_window = None
                            bb_window, bb_std = None, None#bb_param_optomizer_WITHOUT_average(candle_object, op_str, entry_frequency, timebar)
                            candle_object.sma200_double_agent = sm200doubleagent_window_optomizer_WITHOUT_average(candle_object, op_str, entry_frequency, timebar)
                            trending.append({'ticker': candle_object.ticker, 'sector': candle_object.sector,
                                            'mktcap': candle_object.mktcap, 'bb_window': bb_window,
                                            'bb_std': bb_std, 'peers': candle_object.peers, 'ror': ror,
                                            'entry_frequency': entry_frequency, '200sma_double_agent': candle_object.sma200_double_agent})
                            candle_object.df.to_csv(f"{mktcap_group}Stocks/Dataframes/{candle_object.ticker}.csv")
                # except:
                #     continue
        main(self.candles)
        main(self.backup_candles)
        trending_sorted_by_ror = sorted(trending, key=operator.itemgetter('ror'), reverse=True)
        #save results to timestamped json file
        if op_str == '>':
            trend = 'up'
        if op_str == '<':
            trend = 'down'
        with open(f'{mktcap_group}Stocks/Watchlists/{time_markers[-1:]}D-{trend}trend.json', 'w') as outfile:
            json.dump(trending_sorted_by_ror, outfile, indent=2)

class LiteSecurities(Securities):
    def __init__(self, list_of_candles):
        self.candles = list_of_candles
        self.backup_candles = []


# list = Securities('StockLists/Micro<$50M.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Micro', ror_prioritization_factor=1)
# list = Securities('StockLists/Small$50M-$300M.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Small', ror_prioritization_factor=1)
# list = Securities('StockLists/Medium$300M-$2B.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Medium', ror_prioritization_factor=1)
# list = Securities('StockLists/Large$2B-$10B.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='Large', ror_prioritization_factor=1)
# list = Securities('StockLists/VeryLarge>$10B.csv')
# # list = Securities('StockLists/verylargesample.csv')
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
# list.trend_9SMA_20SMA_50SMA_200SMA(1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=1)
