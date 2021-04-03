# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on twitter.

Allow for crypto functionality as well... shouldn't be hard with finnhub cryptocandles.

100 holdings, 1 week turnover = 20 / day...

Add average time in entry zone functionality from entry counter function (currently not factoring that in) *****Important!

Next Steps for Trading Functionality:

Risk Parameters for Trading:
Macro:
1) 70%Long, 30%Short during bull markets... right now is bull market (flip for bear markets)
2) 10% Max Sector Exposure
3) 12 trades per day max, 8 Long, 4 Short
4) 1% account value per stock

Micro:
1) Trailing stops for all, prob ATR... append to watchlist values during nightly scans.
2) Timed exits... set maximum holding period = to interval length (7 calendar days for interval 5, 14 for interval 10, etc)
3) Opposing bollinger exits, average days outside bollinger? Think these through a bit.

***Nothing is set in stone, doesn't have to be perfect just yet. Just get prototype up and running.  

Next step: ATR Trailing Stops, timed exits, bollinger exits.

Also: Will need backup API for finnhub down periods... (need industry data)

Top Insights to address:
1) Allow Long/Short Allocation Ratio to fluctuate with the ratio of uptrending/downtrending
2) Increase entry frequency proportional to rate of return... prioritize the strongest trends.
  The current strategy will favor lower rate of return stocks since the higher ror stocks will hug the upper bound...
  CRITICAL FLAW NEEDS ADDRESSING
