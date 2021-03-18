# chartposting_stocktwits_bot
The main program will automatically post trade setups with charts throughout the market day on stocktwits and twitter.

I need to figure out a way to algorithmically determine support levels for uptrending stocks and resistance
levels for downtrending stocks.

2 Options:
1 EASY) Determine percentage above or below most significant moving average for overall market indicies
and scan for those hits... those hits will trigger scans for individual stocks below some generic MA, either
20SMA or 9SMA most likely... maybe trade allocation depends on MA timeframe... plays into the risk on
risk off macro envirnoment... Pro: Easy to implement Con: Less frequency.

2 HARD) Algorithmically calculate percentage above or below MA for each screened stock...
Will need to research curve fitting and determine a standard deviation from the mean for entries...
....This can be done with bollinger bands... I should be able to determine entry points using
rolling short term standard deviation for stocks trending above all related moving averages, this will update
automatically and wont require periodic scans.

Solution>>> Short term rolling stdev for entry... figure out period and std.

(Keep Marketwide selloff days in back of mind)

Next Step) Determine how many entry signals each year for each stock on average depending on desired
option duration and optimize bollinger parameters for the desired signal frequency


Now that I have an entry counter, for inputed conditions I should be able to
algorithmically  tweak my parameters for the frequency of signals I'd like
generated. Next steps in order priority:
0) Enable continuous successful scan for trending stocks, excepts for all errors,
discovered so far.
1) Determine parameters for desired frequency, learn about the nitty gritty of
bollinger band variables, research theory.
2) Scan that list throughout the day for entries
3) Print and save chart in folder
4) Publish chart to stocktwits and twitter with related tickers and description
