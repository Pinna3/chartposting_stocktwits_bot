# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on twitter.

1) Generate weekly lists for shorts and longs (CHECK)
1.a) Determine periods of interest for both by charting hits (CHECK)
2) Scan that list throughout the day for entries (CHECK)
3) Print and save chart in folder (CHECK)
4) Publish chart to twitter with related tickers and description (CHECK)


Next steps:
1) Build in auto entry scanner... calbrate for 12 signals a year if possible (CHECK)
2) Append sector to super strong uptrend list. (CHECK)

Allow for crypto functionality as well... shouldn't be hard with cryptocandles.

Extract stock lists from Barchart for 10M-100M, 100M-1B, 1B-50B, 50B-250B, 250B+ (CHECK)
      Perform trend scans on all. (CHECK)

100 holdings, 1 week turnover = 20 / day...
100 holdings, 2 week turnover = 10 / day...
Narrow down selection with bollingers, and think of other ways too.

Scanning through the same list multiple times? Think that through... create a priority scheme. (CHECK)
(time weighted rankings order prioritization each day)



Add average time in entry zone functionality from entry counter function (currently not factoring that in) *****Important!

Next Step Trading Functionality:

Risk Parameters for Trading:
Macro:
1) 70%Long, 30%Short during bull markets... right now is bull market (flip for bear markets)
2) 10% Max Sector Exposure
3) 12 trades per day max
4) 1% account value per stock

Micro:
1) Trailing stops for all, prob ATR... append to watchlist values during nightly scans.
2) Timed exits... set maximum holding period = to interval length (7 calendar days for interval 5, 14 for interval 10, etc)
3) Opposing bollinger exits, average days outside bollinger? Think these through a bit.

***Nothing is set in stone, doesn't have to be perfect just yet. Just get prototype up and running.  
