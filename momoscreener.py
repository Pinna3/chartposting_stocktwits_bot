# import finnhub
# import pandas as pd
import csv
from time import sleep
from candlestick import DailyCandleDataRT

# # Symbol lookup
# print(finnhub_client.symbol_lookup('apple'))

class OptionableSecurities:
    def __init__(self, csv_source):
        securities = []
        #CSV Database- comprehensive list of optionable stocks obtain from barchart
        with open(csv_source, 'r') as infile:
        	reader = csv.reader(infile)
        	next(reader) #skip the header line
        	for row in reader:
        		ticker = str(row[0])
        		securities.append(ticker)
        securities.pop()
        self.securities = securities

    def __str__(self):
        return f'OptionableSecurities(Length: {len(self.securities)})'
list = OptionableSecurities('optionablestocks.csv')
print(list.securities[:25])
print(len(list.securities))
#
#     #9SMA > 20SMA > 50SMA > 200SMA (Right now) (add up or down trend functionality)
#     def uptrend_weak(self):
#         #scan for weak uptrend_weak
#         #Setup client
#         finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')
#
#         #Break up scans into segments
#         def scan_start_finish(start, finish):
#             trending = []
#             for index, ticker in enumerate(self.securities[start:finish+1]):
#                 sleep(1)
#                 dataframe = DailyCandleDataRT(ticker, 365)
#                 c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = dataframe.df.iloc[-1]
#                 if sma9 > sma20 > sma50 > sma200:
#                     trending.append(ticker)
#                     print(f'{ticker}:{len(trending)})
#                 else:
#                     print(index)
#             with open(f'weak-uptrend[{start}:{finish+1}].txt', 'w') as outfile:
#             	outfile.write(str(trending))
#
#         segment = len(self.securities) / 5
#         scan_start_finish(0, segment)
#         scan_start_finish(segment, 2 * segment)
#         scan_start_finish(2 * segment, 3 * segment)
#         scan_start_finish(3 * segment, 4 * segment)
#         scan_start_finish(4 * segment, 5 * segment)
#
#     #9SMA > 20SMA > 50SMA > 200SMA (Right now and 1 month ago)
#     def uptrend_medium(self):
#         #scan for weak uptrend_weak
#         #Setup client
#         finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')
#
#         #Break up scans into segments
#         def scan_start_finish(start, finish):
#             trending = []
#             for index, ticker in enumerate(self.securities[start:finish+1]):
#                 sleep(1)
#                 dataframe = DailyCandleDataRT(ticker, 365)
#                 c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = dataframe.df.iloc[-1]
#                 c1m, h1m, l1m, o1m, s1m, t1m, v1m, sma91m, sma201m, sma501m, sma2001m = dataframe.df.iloc[-30]
#                 if sma9 > sma20 > sma50 > sma200 and sma91m > sma201m > sma501m > sma2001m:
#                     trending.append(ticker)
#                     print(f'{ticker}:{len(trending)})
#                 else:
#                     print(index)
#             with open(f'medium-uptrend[{start}:{finish+1}].txt', 'w') as outfile:
#             	outfile.write(str(trending))
#
#         segment = len(self.securities) / 5
#         scan_start_finish(0, segment)
#         scan_start_finish(segment, 2 * segment)
#         scan_start_finish(2 * segment, 3 * segment)
#         scan_start_finish(3 * segment, 4 * segment)
#         scan_start_finish(4 * segment, 5 * segment)
#
#     #9SMA > 20SMA > 50SMA > 200SMA (Right now and 1 month ago and 2 months ago)
#     def uptrend_strong(self):
#         #scan for weak uptrend_weak
#         #Setup client
#         finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')
#
#         #Break up scans into segments
#         def scan_start_finish(start, finish):
#             trending = []
#             for index, ticker in enumerate(self.securities[start:finish+1]):
#                 sleep(1)
#                 dataframe = DailyCandleDataRT(ticker, 365)
#                 c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = dataframe.df.iloc[-1]
#                 c1m, h1m, l1m, o1m, s1m, t1m, v1m, sma91m, sma201m, sma501m, sma2001m = dataframe.df.iloc[-30]
#                 c2m, h2m, l2m, o2m, s2m, t2m, v2m, sma92m, sma202m, sma502m, sma2002m = dataframe.df.iloc[-60]
#                 if sma9 > sma20 > sma50 > sma200 and sma91m > sma201m > sma501m > sma2001m and sma92m > sma202m > sma502m > sma2002m:
#                     trending.append(ticker)
#                     print(f'{ticker}:{len(trending)})
#                 else:
#                     print(index)
#             with open(f'strong-uptrend[{start}:{finish+1}].txt', 'w') as outfile:
#             	outfile.write(str(trending))
#
#         segment = len(self.securities) / 5
#         scan_start_finish(0, segment)
#         scan_start_finish(segment, 2 * segment)
#         scan_start_finish(2 * segment, 3 * segment)
#         scan_start_finish(3 * segment, 4 * segment)
#         scan_start_finish(4 * segment, 5 * segment)
#
# #Filter full list for volume and market cap
# class FilteredOptionable(OptionableSecurities):
#     pass
