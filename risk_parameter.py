from utility_func import get_account_value
import json
from glob import glob
from datetime import date
today_date = date.today().strftime('%m-%d-%y')


#expand to all folders
def set_long_short_capacities(watchlists_generation_date):
    long_total = 0
    for file in glob(f'MicroStocks/Watchlists/{watchlists_generation_date}/*uptrend.json'):
        with open(file) as infile:
            content = json.load(infile)
            long_total += len(content)

    short_total = 0
    for file in glob(f'MicroStocks/Watchlists/{watchlists_generation_date}/*downtrend.json'):
        with open(file) as infile:
            content = json.load(infile)
            short_total += len(content)

    return long_total, short_total

print(set_long_short_capacities(today_date))



#70% max long allocation in bull markets
def long_capacity(portfolio_current, max_exposure=69):
    return portfolio_current >= max_exposure

#30% max short allocation in bull markets
def short_capacity(portfolio_current, max_exposure=29):
    return portfolio_current >= max_exposure

#10% max allocation per industry, key error means no sector exposure yet
def industry_capacity(portfolio_current, max_exposure=9):
    return portfolio_current >= max_exposure

# Maximums: 8 x long(3 x verylarge, 2 x large, 1 x medium, 1 x small, 1 x micro),
#          4 x short(2 x verylarge, 1 x large, 1 x medium)
def check_daily_counter_capacity(side, mkt_cap,
                        max_long=8, max_short=4,
                        max_long_verylarge=3, max_long_large=2, max_long_medium=1, max_long_small=1, max_long_micro=1,
                        max_short_verylarge=2, max_short_large=1, max_short_medium=1, max_short_small=0, max_short_micro=0):
    with open('DailyCounter.json') as infile:
        counter = json.load(infile)
        if counter['today_date'] == today_date:
            if side == 'long' and mkt_cap == 'VeryLarge':
                if counter['long'] < max_long and counter['long_mkt_cap']['VeryLarge'] < max_long_verylarge:
                    return False
            elif side == 'long' and mkt_cap == 'Large':
                if counter['long'] < max_long and counter['long_mkt_cap']['Large'] < max_long_large:
                    return False
            elif side == 'long' and mkt_cap == 'Medium':
                if counter['long'] < max_long and counter['long_mkt_cap']['Medium'] < max_long_medium:
                    return False
            elif side == 'long' and mkt_cap == 'Small':
                if counter['long'] < max_long and counter['long_mkt_cap']['Small'] < max_long_small:
                    return False
            elif side == 'long' and mkt_cap == 'Micro':
                if counter['long'] < max_long and counter['long_mkt_cap']['Micro'] < max_long_micro:
                    return False

            if side == 'short' and mkt_cap == 'Verylarge':
                if counter['short'] < max_short and counter['short_mkt_cap']['VeryLarge'] < max_short_verylarge:
                    return False
            elif side == 'short' and mkt_cap == 'Large':
                if counter['short'] < max_short and counter['short_mkt_cap']['Large'] < max_short_large:
                    return False
            elif side == 'short' and mkt_cap == 'Medium':
                if counter['short'] < max_short and counter['short_mkt_cap']['Medium'] < max_short_medium:
                    return False
            elif side == 'short' and mkt_cap == 'Small':
                if counter['short'] < max_short and counter['short_mkt_cap']['Small'] < max_short_small:
                    return False
            elif side == 'short' and mkt_cap == 'Micro':
                if counter['short'] < max_short and counter['short_mkt_cap']['Micro'] < max_short_micro:
                    return False
            else:
                return True
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
