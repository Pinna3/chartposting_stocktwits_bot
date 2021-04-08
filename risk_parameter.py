from utility_func import get_account_value
import json
from glob import glob
from datetime import date
today_date = date.today().strftime('%m-%d-%y')

#expand to all folders
def set_long_short_capacities():
    mkt_caps = ['MicroStocks', 'SmallStocks', 'MediumStocks', 'LargeStocks', 'VeryLargeStocks']
    long_total = 0
    for group in mkt_caps:
        for file in glob(f'{group}/Watchlists/*uptrend.json'):
            with open(file) as infile:
                content = json.load(infile)
                long_total += len(content)

    short_total = 0
    for group in mkt_caps:
        for file in glob(f'{group}/Watchlists/*downtrend.json'):
            with open(file) as infile:
                content = json.load(infile)
                short_total += len(content)

    long_max_exposure = round((long_total / (long_total + short_total) * 100))
    short_max_exposure = round((short_total / (long_total + short_total) * 100))
    print(f"Long Max Exposure: {long_max_exposure}%, Short Max Exposure: {short_max_exposure}%, Long Total: {long_total}, Short Total: {short_total}")
    return long_max_exposure, short_max_exposure

#70% max long allocation in bull markets
def long_capacity(portfolio_current):
    long_max_exposure, short_max_exposure = set_long_short_capacities()
    return portfolio_current >= long_max_exposure

#30% max short allocation in bull markets
def short_capacity(portfolio_current):
    long_max_exposure, short_max_exposure = set_long_short_capacities()
    return portfolio_current >= short_max_exposure

#10% max allocation per sector, key error means no sector exposure yet
def sector_capacity(portfolio_current, max_exposure=9):
    return abs(portfolio_current) >= max_exposure

# Maximums: 8 x long(3 x verylarge, 2 x large, 1 x medium, 1 x small, 1 x micro),
#          4 x short(2 x verylarge, 1 x large, 1 x medium)
def check_daily_counter_capacity(side, mkt_cap, max_daily_trades=12,
                        max_long_verylarge=.25, max_long_large=.25, max_long_medium=.25, max_long_small=.125, max_long_micro=.125,
                        max_short_verylarge=.50, max_short_large=.25, max_short_medium=.25, max_short_small=0, max_short_micro=0):

    long_max_exposure, short_max_exposure = set_long_short_capacities()
    max_long = round((long_max_exposure / 100) * max_daily_trades)
    max_short = round((short_max_exposure / 100)* max_daily_trades)

    mktcap_groups  = ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']
    mktcap_long_maxes = [max_long_verylarge, max_long_large, max_long_medium, max_long_small, max_long_micro]
    mktcap_short_maxes = [max_short_verylarge, max_short_large, max_short_medium,  max_short_small, max_short_micro]
    long_mkt_cap_or_short_mkt_cap = f'{side}_mkt_cap'

    if side == 'long':
        max = max_long
        for mktcap, mktcap_max in zip(mktcap_groups, mktcap_long_maxes):
            if mkt_cap == mktcap:
                fraction = mktcap_max

    elif side == 'short':
        max = max_short
        for mktcap, mktcap_max in zip(mktcap_groups, mktcap_short_maxes):
            if mkt_cap == mktcap:
                fraction = mktcap_max

    def daily_counter_test(side, mktcap, max, fraction, long_mkt_cap_or_short_mkt_cap):
        maximum_count = round(fraction * max)
        if counter[side] < max and counter[long_mkt_cap_or_short_mkt_cap][mktcap] < maximum_count:
            return False
        else:
            return True

    #make sure Daily Counter is working
    print(f"\n\nDaily Counter Capacities:\n\nLong: {max_long}, VeryLarge: {max_long_verylarge*max_long}, Large: {max_long_large*max_long}, \
            Medium: {max_long_medium*max_long}, Small: {max_long_small*max_long}, Micro: {max_long_micro*max_long}\n\n \
            Short: {max_short}, VeryLarge: {max_short_verylarge*max_short}, Large: {max_short_large*max_short}, Medium: {max_short_medium*max_short}, \
            Small: {max_short_small*max_short}, Micro: {max_short_micro*max_short}")

    with open('DailyCounter.json') as infile:
        counter = json.load(infile)
        if counter['today_date'] == today_date:
            return daily_counter_test(side, mkt_cap, max, fraction, long_mkt_cap_or_short_mkt_cap)
        else:
            return False

#Checks to make sure date is current, if so adds to daily tally.
#If its the first trade of the day it erases yesterday tally and starts fresh.
def add_to_daily_counter(side, mkt_cap):
    with open('DailyCounter.json') as infile:
        counter = json.load(infile)
        if counter['today_date'] != today_date:
            counter = {
                'today_date': today_date,
                'long': 0,
                'long_mkt_cap': {
                    'VeryLarge': 0,
                    'Large': 0,
                    'Medium': 0,
                    'Small': 0,
                    'Micro': 0
                    },
                'short': 0,
                'short_mkt_cap': {
                    'VeryLarge': 0,
                    'Large': 0,
                    'Medium': 0,
                    'Small': 0,
                    'Micro': 0
                    }
                }
        counter[side] += 1
        counter[f'{side}_mkt_cap'][mkt_cap] += 1
    with open('DailyCounter.json', 'w') as outfile:
        json.dump(counter, outfile, indent=2)

#Checks to make sure date is current, if so adds to daily tally.
#If its the first trade of the day it erases yesterday tally and starts fresh.
def add_to_daily_tradelist(symbol):
    with open('DailyTrades.json') as infile:
        trades = json.load(infile)
        if trades['today_date'] != today_date:
            trades = {
                'today_date': today_date,
                'trades': []}
            trades['trades'].append(symbol)
        else:
            trades['trades'].append(symbol)
    with open('DailyTrades.json', 'w') as outfile:
        json.dump(trades, outfile, indent=2)

def check_daily_tradelist(symbol):
    with open('DailyTrades.json') as infile:
        trades = json.load(infile)
        if trades['today_date'] != today_date:
            return False
        else:
            return symbol in trades['trades']
