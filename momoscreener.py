# import finnhub
# import pandas as pd
import csv
from time import sleep
from candlestick import DailyCandleDataRT

# #Setup client
# finnhub_client = finnhub.Client(api_key='c17qcvf48v6sj55b3t9g')

# # Symbol lookup
# print(finnhub_client.symbol_lookup('apple'))

#CSV Database- comprehensive list of optionable stocks obtain from barchart
stripped_optionable = []
with open('optionablestocks.csv', 'r') as infile:
	reader = csv.reader(infile)
	next(reader) #skip the header line
	for row in reader:
		ticker = str(row[0])
		stripped_optionable.append(ticker)

stripped_optionable.pop()
# print(stripped_optionable)

#scan for MA trending up

trending = []
for ticker in stripped_optionable[90:100]:
    sleep(1)
    dataframe = DailyCandleDataRT(ticker, 365)
    c, h, l, o, s, t, v, sma9, sma20, sma50, sma200 = dataframe.df.iloc[-1]
    if sma9 > sma20 > sma50 > sma200:
        trending.append(ticker)
        print(len(trending))
    else:
        print('.')
with open('strong-uptrend.txt', 'w') as outfile:
	outfile.write(str(trending))
