# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on stocktwits and twitter.

1) Generate weekly lists for shorts and longs
1.a) Determine periods of interest for both by charting hits
2) Scan that list throughout the day for entries
3) Print and save chart in folder
4) Publish chart to stocktwits and twitter with related tickers and description


Next steps:
1) Build in auto entry scanner... calbrate for 12 signals a year if possible
2) Append sector to super strong uptrend list.


ADD CACHE (MEMOIZE) TO AVOID QUERYING MORE THAN NECESSARY, CUT TIME DOWN SIGNIFICANTLY.

Ok, I'm a little lost here. So what do I have? I have the ability to scan ~5000 optionable
stocks for downtrends and uptrends... (run downtrend scan when eating my soup) and the ability
to append that final list with industry data and bollinger parameters seperately,
so lets combine those. Ok, I coombined those into one function...

So now after after a couple nights of running scans, soon to be 1 night, I will
have 1 list of stock dictionaries with all the necessary info required to scan throughout
the day for entries (adjust scans to make quicker, narrow parameters and utilize memoize  
  i.e. caching). So that is the next step... set up the main program to do that.
