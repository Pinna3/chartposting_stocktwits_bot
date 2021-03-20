import finnhub
import csv
from time import sleep
from candlestick import DailyCandleDataRT
import json
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')


class OptionableSecurities:
    def __init__(self, csv_source):
        securities = []
        # CSV Database- comprehensive list of optionable stocks obtain from barchart
        with open(csv_source, 'r') as infile:
            reader = csv.reader(infile)
            next(reader)  # skip the header line
            for row in reader:
                ticker = str(row[0])
                securities.append(ticker)
        securities.pop()
        self.securities = securities

    def __str__(self):
        return f'OptionableSecurities(Length: {len(self.securities)})'

    # 9SMA > 20SMA > 50SMA > 200SMA (Right now) (add up or down trend functionality)
    def uptrend_weak(self):
        # scan for weak uptrend_weak
        # Setup client
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        trending = []
        for index, ticker in enumerate(self.securities):
            sleep(1)
            try:
                dataframe = DailyCandleDataRT(ticker, 365, 20, 2)
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = dataframe.df.iloc[-1]
                if sma9 > sma20 > sma50 > sma200:
                    trending.append(ticker)
                    print(f'{ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        with open(f'weak-uptrend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)


    # 9SMA > 20SMA > 50SMA > 200SMA (Right now and 1 month ago)
    def uptrend_medium(self):
        # scan for weak uptrend_weak
        # Setup client
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        trending = []
        for index, ticker in enumerate(self.securities):
            sleep(1)
            try:
                dataframe = DailyCandleDataRT(ticker, 365, 20, 2)
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = dataframe.df.iloc[-1]
                c1m, h1m, l1m, o1m, s1m, t1m, v1m, sma91m, sma201m, sma501m, sma2001m, lower, upper = dataframe.df.iloc[-30]
                if sma9 > sma20 > sma50 > sma200 and sma91m > sma201m > sma501m > sma2001m:
                    trending.append(ticker)
                    print(f'{ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        with open(f'medium-uptrend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)


    # 9SMA > 20SMA > 50SMA > 200SMA (Right now and 1 month ago and 2 months ago)
    def uptrend_strong(self):
        # scan for weak uptrend_weak
        # Setup client
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        trending = []
        for index, ticker in enumerate(self.securities):
            sleep(1)
            try:
                dataframe = DailyCandleDataRT(ticker, 365, 20, 2)
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = dataframe.df.iloc[-1]
                c1m, h1m, l1m, o1m, s1m, t1m, v1m, sma91m, sma201m, sma501m, sma2001m, lower, upper = dataframe.df.iloc[-30]
                c2m, h2m, l2m, o2m, s2m, t2m, v2m, sma92m, sma202m, sma502m, sma2002m, lower, upper = dataframe.df.iloc[-60]
                if sma9 > sma20 > sma50 > sma200 and sma91m > sma201m > sma501m > sma2001m and sma92m > sma202m > sma502m > sma2002m:
                    trending.append(ticker)
                    print(f'{ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        with open(f'strong-uptrend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)


    # 9SMA > 20SMA > 50SMA > 200SMA (Right now and .5, 1, 1.5, 2, 2.5, 3 months ago)
    def uptrend_superstrong(self):
        # scan for weak uptrend_weak
        # Setup client
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')

        trending = []
        for index, ticker in enumerate(self.securities):
            sleep(1)
            try:
                dataframe = DailyCandleDataRT(ticker, 365, 20, 2)
                c, h, l, o, s, t, v, sma9, sma20, sma50, sma200, lower, upper = dataframe.df.iloc[-1]
                c2w, h2w, l2w, o2w, s2w, t2w, v2w, sma92w, sma202w, sma502w, sma2002w, lower, upper = dataframe.df.iloc[-15]
                c4w, h4w, l4w, o4w, s4w, t4w, v4w, sma94w, sma204w, sma504w, sma2004w, lower, upper = dataframe.df.iloc[-30]
                c6w, h6w, l6w, o6w, s6w, t6w, v6w, sma96w, sma206w, sma506w, sma2006w, lower, upper = dataframe.df.iloc[-45]
                c8w, h8w, l8w, o8w, s8w, t8w, v8w, sma98w, sma208w, sma508w, sma2008w, lower, upper = dataframe.df.iloc[-60]
                c10w, h10w, l10w, o10w, s10w, t10w, v10w, sma910w, sma2010w, sma5010w, sma20010w, lower, upper = dataframe.df.iloc[-75]
                c12w, h12w, l12w, o12w, s12w, t12w, v12w, sma912w, sma2012w, sma5012w, sma20012w, lower, upper = dataframe.df.iloc[-90]
                if sma9 > sma20 > sma50 > sma200 and sma92w > sma202w > sma502w > sma2002w and sma94w > sma204w > sma504w > sma2004w and \
                    sma96w > sma206w > sma506w > sma2006w and sma98w > sma208w > sma508w > sma2008w and sma910w > sma2010w > sma5010w > sma20010w \
                    and sma912w > sma2012w > sma5012w > sma20012w:
                    trending.append(ticker)
                    print(f'{ticker}:{len(trending)}')
                else:
                    print(index)
            except:
                continue
        with open(f'superstrong-uptrend{today_date}.json', 'w') as outfile:
            json.dump(trending, outfile, indent=2)


# Filter full list for volume and market cap
class FilteredOptionable(OptionableSecurities):
    def __init__(self, csv_source, min_mktcap, min_volume):
        securities = []
        # CSV Database- comprehensive list of optionable stocks obtain from barchart
        with open(csv_source, 'r') as infile:
            reader = csv.reader(infile)
            next(reader)  # skip the header line
            for row in reader:
                ticker = str(row[0])
                if row[2] != 'N/A' and row[2] != '':
                    mkt_cap = float(row[2])
                if row[3] != 'N/A' and row[3] != '':
                    volume = float(row[3])
                if mkt_cap > min_mktcap and volume > min_volume:
                    securities.append(ticker)
        self.securities = securities

list = OptionableSecurities('optionablestocks.csv')
list.uptrend_strong()
