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
