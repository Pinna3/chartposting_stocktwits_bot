# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on twitter.

Allow for crypto functionality as well... shouldn't be hard with finnhub cryptocandles.

100 holdings, 1 week turnover = 20 / day...

Add average time in entry zone functionality from entry counter function (currently not factoring that in) *****Important!

Next Steps for Trading Functionality:

*Opposing bollinger exits, average days outside bollinger? Think these through a bit.

***Nothing is set in stone, doesn't have to be perfect just yet. Just get prototype up and running.  

Next step: Bollinger exits.

Top Insights to address:
1) Increase entry frequency proportional to rate of return... prioritize the strongest trends.
  The current strategy will favor lower rate of return stocks since the higher ror stocks will hug the upper bound...
  CRITICAL FLAW NEEDS ADDRESSING
2) Think about using shifting ATR values to optimize ATR stop multiples (For now, use trailing stops of 1ATR[placeholder])

[Should address]
3+) Think about Priority Scheme
4+) Clean up some code, a little every day... must be done.

***I'm starting to think I should have the program buy the very best trenders in the very lowest dropoff rate periods on opposite to trend days as
some sort of position initializing function, then buy and sell stragglers throughout the remainder of the period... reaccess at regular intervals...

Initialization: Buy/Short ~100 positions according to the daily counter ratios...
Maintenance: Buy/Short top trenders not in holdings to fill in the gaps... prioritizing the highest rate of returns
Re-Initialization: Sell holdings that no longer make the cut, add new ones that do.
Maintenance: rinse and repeat every week or so.
***This make more sense to me and seems to prioritize the top trenders better.

Now work on exit strategy... or do we really need one with trailing stops? Prob should implement something else, think about it.
