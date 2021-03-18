# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on stocktwits and twitter.

1) Optimize bollinger band smoothing length for desired hit frequency (add data to ticker list)
2) Determine average number of days below or above bollinger band
3) Add downtrending functionality


Now that I have an entry counter, for inputed conditions I should be able to
algorithmically  tweak my bollinger smoothing length parameter for the frequency
of signals I'd like generated. Next steps in order priority:
0) Enable continuous successful scan for trending stocks, excepts for all errors,
discovered so far.
1) Determine parameters for desired frequency, learn about the nitty gritty of
bollinger band variables, research theory.
2) Scan that list throughout the day for entries
3) Print and save chart in folder
4) Publish chart to stocktwits and twitter with related tickers and description
