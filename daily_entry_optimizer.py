import json, csv
import pandas as pd
from risk_parameter import preset_daily_counter_capacities, set_long_short_capacities
from utility_func import pull_top_tier_unbroken_trenders, get_all_portfolio_tickers
from candlestick import LiteSecurityTradeData, SecurityTradeData
from momoscreener import LiteSecurities
from alpaca import get_all_positions
from glob import glob

def construct_dict_of_top_tier_unbroken_trenders(tier_percentage=12):
    trender_watchlist_filenames = pull_top_tier_unbroken_trenders(tier_percentage)
    list_of_almost_consumable_lists = []
    for filename in trender_watchlist_filenames:
        if filename is not None:
            with open(filename[0]) as infile:
                watchlist = json.load(infile)
                consumable_list_plus_side = []
                for stock in watchlist:
                    if stock['ticker'] not in get_all_portfolio_tickers():
                        ticker = stock['ticker']
                        sector = stock['sector']
                        peers = stock['peers']
                        mktcap = stock['mktcap']
                        smoothness = 'TRUE'
                        # bb_window = stock["bb_window"]
                        # bb_std = stock['bb_std']
                        sma200_double_agent = stock['200sma_double_agent']
                        df = pd.read_csv(f"{mktcap}Stocks/Dataframes/{ticker}.csv", index_col=0)
                        if 'uptrend' in filename[0]:
                            opt_str = '>'
                        elif 'downtrend' in filename[0]:
                            opt_str = '<'
                        consumable_list_plus_side.append([opt_str, ticker, mktcap, sector, smoothness, peers, sma200_double_agent, df])
            list_of_almost_consumable_lists.append(consumable_list_plus_side)
    candle_object_list_dict = {
        '>': {
            'VeryLarge' : [],
            'Large': [],
            'Medium': [],
            'Small': [],
            'Micro': []
        },
        '<': {
            'VeryLarge' : [],
            'Large': [],
            'Medium': [],
            'Small': [],
            'Micro': []
        }
    }
    for almost_consumable_list in list_of_almost_consumable_lists:
        for almost_consumable_item in almost_consumable_list:
            candle_object_list_dict[almost_consumable_item[0]][almost_consumable_item[2]].append(LiteSecurityTradeData(almost_consumable_item[1:]))
    return candle_object_list_dict

#minimum ror_prioritization_factor is 1
def optimal_ror_prioritization_factor_for_nightly_scan_input(candle_object_list_dict, op_str, mktcap_group, title_time_marker, ror_prioritization_factor=2):
    candles = LiteSecurities(candle_object_list_dict[op_str][mktcap_group])
    candles.trend_9SMA_20SMA_50SMA_200SMA(title_time_marker, op_str, mktcap_group, ror_prioritization_factor)
    hits = 0
    for candle in candle_object_list_dict[op_str][mktcap_group]:
        candle.sma200_double_agent_activate(candle.sma200_double_agent)
        c, h, l, o, v, sma9, sma20, sma50, sma200, lower, upper, atr = candle.df.iloc[-1]
        if op_str == '>':
            if l < sma200:
                hits += 1
        elif op_str == '<':
            if h > sma200:
                hits += 1
        candle.sma200_double_agent_activate(200)
    return (hits, len(candle_object_list_dict[op_str][mktcap_group]))

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
def open_capacities_dict():
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
            'VeryLarge' : long_verylarge,
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
# print(open_capacities_dict())

capacities_dict = open_capacities_dict()
candle_object_list_dict = construct_dict_of_top_tier_unbroken_trenders(tier_percentage=12)
# print(candle_object_list_dict['>']['VeryLarge'][1].sma200_double_agent)
top_tier_trenders = pull_top_tier_unbroken_trenders(tier_percentage=12)
for filename, timemarker, mktcap, op_str, num, total in [trender for trender in top_tier_trenders if trender != None]:
    print(filename, num, total)
    priority_factor_range = [i/10 for i in range(10, 51)]
    for ror_priority_factor in priority_factor_range:
        hits, category_total = optimal_ror_prioritization_factor_for_nightly_scan_input(candle_object_list_dict, op_str, mktcap, timemarker, ror_prioritization_factor=ror_priority_factor)
        if hits >= capacities_dict[op_str][mktcap]:
            print(hits, ror_priority_factor)
            break
    print(hits, ror_priority_factor)
