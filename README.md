# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on twitter.

Allow for crypto functionality as well... shouldn't be hard with cryptocandles.

100 holdings, 1 week turnover = 20 / day...
100 holdings, 2 week turnover = 10 / day...
Narrow down selection with bollingers, and think of other ways too.

Add average time in entry zone functionality from entry counter function (currently not factoring that in) *****Important!

Think of other ways to narrow selection other than bollingers, rate of increase would be good.

Next Steps for Trading Functionality:

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
