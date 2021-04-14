from alpaca import get_all_positions, get_account_value
import json, csv
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
    return long_max_exposure, short_max_exposure, long_total, short_total

#70% max long allocation in bull markets
def check_long_capacity(portfolio_current):
    long_max_exposure, short_max_exposure, long_total, short_total = set_long_short_capacities()
    return portfolio_current >= long_max_exposure

#30% max short allocation in bull markets
def check_short_capacity(portfolio_current):
    long_max_exposure, short_max_exposure, long_total, short_total = set_long_short_capacities()
    return portfolio_current >= short_max_exposure

#10% max allocation per sector, key error means no sector exposure yet
def sector_capacity(portfolio_current, max_exposure=11):
    return abs(portfolio_current) >= max_exposure

###These can change with market conditions as well... play with it...
###if long/short = 75/25 then...
###if long/short = 50/50 then... (add ratios make numbers work)
def preset_daily_counter_capacities():
    daily_counter_capacities = {
        'max_daily_trades': 15,
        'max_long_verylarge': .25,
        'max_long_large': .25,
        'max_long_medium': .20,
        'max_long_small': .15,
        'max_long_micro': .15,
        'max_short_verylarge': .40,
        'max_short_large': .40,
        'max_short_medium': .10,
        'max_short_small': 0,
        'max_short_micro': 0
    }
    return daily_counter_capacities

def print_daily_counter_capacities():
    daily_counter_capacities = preset_daily_counter_capacities()
    max_daily_trades = daily_counter_capacities['max_daily_trades']
    max_long_verylarge = daily_counter_capacities['max_long_verylarge']
    max_long_large = daily_counter_capacities['max_long_large']
    max_long_medium = daily_counter_capacities['max_long_medium']
    max_long_small = daily_counter_capacities['max_long_small']
    max_long_micro = daily_counter_capacities['max_long_micro']
    max_short_verylarge = daily_counter_capacities['max_short_verylarge']
    max_short_large = daily_counter_capacities['max_short_large']
    max_short_medium = daily_counter_capacities['max_short_medium']
    max_short_small = daily_counter_capacities['max_short_small']
    max_short_micro = daily_counter_capacities['max_short_micro']

    long_max_exposure, short_max_exposure, long_total, short_total = set_long_short_capacities()
    max_long = round((long_max_exposure / 100) * max_daily_trades)
    max_short = round((short_max_exposure / 100)* max_daily_trades)

    print(f"""
Daily Counter Capacities:
Long: {max_long}, VeryLarge: {round(max_long_verylarge*max_long)}, Large: {round(max_long_large*max_long)}, Medium: {round(max_long_medium*max_long)}, Small: {round(max_long_small*max_long)}, Micro: {round(max_long_micro*max_long)}
Short: {max_short}, VeryLarge: {round(max_short_verylarge*max_short)}, Large: {round(max_short_large*max_short)}, Medium: {round(max_short_medium*max_short)}, Small: {round(max_short_small*max_short)}, Micro: {round(max_short_micro*max_short)}
Long Max Exposure: {long_max_exposure}%, Short Max Exposure: {short_max_exposure}%, Long Total: {long_total}, Short Total: {short_total}
""")

def check_daily_counter_capacity(side, mkt_cap):
    daily_counter_capacities = preset_daily_counter_capacities()
    max_daily_trades = daily_counter_capacities['max_daily_trades']
    max_long_verylarge = daily_counter_capacities['max_long_verylarge']
    max_long_large = daily_counter_capacities['max_long_large']
    max_long_medium = daily_counter_capacities['max_long_medium']
    max_long_small = daily_counter_capacities['max_long_small']
    max_long_micro = daily_counter_capacities['max_long_micro']
    max_short_verylarge = daily_counter_capacities['max_short_verylarge']
    max_short_large = daily_counter_capacities['max_short_large']
    max_short_medium = daily_counter_capacities['max_short_medium']
    max_short_small = daily_counter_capacities['max_short_small']
    max_short_micro = daily_counter_capacities['max_short_micro']

    long_max_exposure, short_max_exposure, long_total, short_total = set_long_short_capacities()
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

    with open('DailyCounter.json') as infile:
        counter = json.load(infile)
        if counter['today_date'] == today_date:
            return daily_counter_test(side, mkt_cap, max, fraction, long_mkt_cap_or_short_mkt_cap)
        else:
            return False

# check_daily_counter_capacity('long', 'VeryLarge')
# print(preset_daily_counter_capacities())

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

def categorize_open_positions():
    all_positions = get_all_positions()
    long_positions = []
    long_verylarge, long_large, long_medium, long_small, long_micro = 0, 0, 0, 0, 0
    short_positions = []
    short_verylarge, short_large, short_medium, short_small, short_micro = 0, 0, 0, 0, 0
    [long_positions.append(position['symbol']) for position in all_positions if position['side'] == 'long']
    [short_positions.append(position['symbol']) for position in all_positions if position['side'] == 'short']
    with open('StockLists/VeryLarge>$10B.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        very_large = [row[0] for row in reader]
        for ticker in long_positions:
            if ticker in very_large:
                long_verylarge += 1
        for ticker in short_positions:
            if ticker in very_large:
                short_verylarge += 1
    with open('StockLists/Large$2B-$10B.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        large = [row[0] for row in reader]
        for ticker in long_positions:
            if ticker in large:
                long_large += 1
        for ticker in short_positions:
            if ticker in large:
                short_large += 1
    with open('StockLists/Medium$300M-$2B.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        medium = [row[0] for row in reader]
        for ticker in long_positions:
            if ticker in medium:
                long_medium += 1
        for ticker in short_positions:
            if ticker in medium:
                short_medium += 1
    with open('StockLists/Small$50M-$300M.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        small = [row[0] for row in reader]
        for ticker in long_positions:
            if ticker in small:
                long_small += 1
        for ticker in short_positions:
            if ticker in small:
                short_small += 1
    with open('StockLists/Micro<$50M.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        micro = [row[0] for row in reader]
        for ticker in long_positions:
            if ticker in micro:
                long_micro += 1
        for ticker in short_positions:
            if ticker in micro:
                short_micro += 1
    return long_verylarge, long_large, long_medium, long_small, long_micro, short_verylarge, short_large, short_medium, short_small, short_micro

#open capacities factoring in account holdings
def open_mktcap_capacities_dict():
    long_max_exposure, short_max_exposure, long_total, short_total = set_long_short_capacities()
    capacities = preset_daily_counter_capacities()
    long_verylarge_acct, long_large_acct, long_medium_acct, long_small_acct, long_micro_acct, short_verylarge_acct, short_large_acct, short_medium_acct, short_small_acct, short_micro_acct = categorize_open_positions()
    long_verylarge = round(capacities['max_long_verylarge'] * long_max_exposure - long_verylarge_acct)
    long_large = round(capacities['max_long_large'] * long_max_exposure - long_large_acct)
    long_medium = round(capacities['max_long_medium'] * long_max_exposure - long_medium_acct)
    long_small = round(capacities['max_long_small'] * long_max_exposure - long_small_acct)
    long_micro = round(capacities['max_long_micro'] * long_max_exposure - long_micro_acct)
    short_verylarge = round(capacities['max_short_verylarge'] * short_max_exposure - short_verylarge_acct)
    short_large = round(capacities['max_short_large'] * short_max_exposure - short_large_acct)
    short_medium = round(capacities['max_short_medium'] * short_max_exposure - short_medium_acct)
    short_small = round(capacities['max_short_small'] * short_max_exposure - short_small_acct)
    short_micro = round(capacities['max_short_micro'] * short_max_exposure - short_micro_acct)
    capacities_dict = {
        '>': {
            'VeryLarge': long_verylarge,
            'Large': long_large,
            'Medium': long_medium,
            'Small': long_small,
            'Micro': long_micro
        },
        '<': {
            'VeryLarge' : short_verylarge,
            'Large': short_large,
            'Medium': short_medium,
            'Small': short_small,
            'Micro': short_micro
        }
    }
    return capacities_dict
# print(open_mktcap_capacities_dict())
# print('')

def open_sector_capacities_dict():
    with open('SectorAllocationDict.json') as infile:
        dict = json.load(infile)

    sector_percentage_capacities_dict = {
        '>': {
            'Consumer Services': 12,
            'Consumer Non-Durables': 12,
            'Basic Industries': 12,
            'Consumer Durables': 12,
            'Energy': 12,
            'Transportation': 12,
            'Technology': 12,
            'Health Care': 12,
            'Public Utilities': 12,
            'Finance': 12,
            'Capital Goods': 12,
            'Miscellaneous': 12
        },
        '<': {
            'Consumer Services': 12,
            'Consumer Non-Durables': 12,
            'Basic Industries': 12,
            'Consumer Durables': 12,
            'Energy': 12,
            'Transportation': 12,
            'Technology': 12,
            'Health Care': 12,
            'Public Utilities': 12,
            'Finance': 12,
            'Capital Goods': 12,
            'Miscellaneous': 12
        }
    }
    for sector in dict['long']['sector'].keys():
        sector_percentage_capacities_dict['>'][sector] -= round(dict['long']['sector'][sector]['acct_percentage'])
    for sector in dict['short']['sector'].keys():
        sector_percentage_capacities_dict['<'][sector] -= round(dict['short']['sector'][sector]['acct_percentage'])

    return sector_percentage_capacities_dict
# print(open_sector_capacities_dict())
