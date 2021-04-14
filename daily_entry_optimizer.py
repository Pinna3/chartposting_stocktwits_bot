import json, csv
import pandas as pd
from risk_parameter import preset_daily_counter_capacities, set_long_short_capacities, open_mktcap_capacities_dict
from utility_func import pull_top_tier_unbroken_trenders
from candlestick import LiteSecurityTradeData, SecurityTradeData
from momoscreener import LiteSecurities
from alpaca import get_all_positions, get_all_portfolio_tickers
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

def optimized_prioritization_factors():
    capacities_dict = open_mktcap_capacities_dict()
    candle_object_list_dict = construct_dict_of_top_tier_unbroken_trenders(tier_percentage=12)
    top_tier_trenders = pull_top_tier_unbroken_trenders(tier_percentage=12)
    ror_prioritization_dict = {
        '>': {
            'VeryLarge' : 1.0,
            'Large': 1.0,
            'Medium': 1.0,
            'Small': 1.0,
            'Micro': 1.0
        },
        '<': {
            'VeryLarge' : 1.0,
            'Large': 1.0,
            'Medium': 1.0,
            'Small': 1.0,
            'Micro': 1.0
        }
    }
    def return_priority_factor_if_capacity_is_met(candle_object_list_dict, op_str, mktcap, timemarker):
        priority_factor_range = [i/10 for i in range(10, 51)]
        for ror_priority_factor in priority_factor_range:
            hits, category_total = optimal_ror_prioritization_factor_for_nightly_scan_input(candle_object_list_dict, op_str, mktcap, timemarker, ror_prioritization_factor=ror_priority_factor)
            print(hits)
            if hits >= capacities_dict[op_str][mktcap] or hits == category_total:
                return ror_priority_factor
        return ror_priority_factor

    for filename, timemarker, mktcap, op_str, num, total in [trender for trender in top_tier_trenders if trender is not None]:
        print(filename, num, total)
        print(capacities_dict)
        print('')
        ror_prioritization_dict[op_str][mktcap] = return_priority_factor_if_capacity_is_met(candle_object_list_dict, op_str, mktcap, timemarker)

            #     print(hits)
            #     continue
            # else:
            #     ror_prioritization_dict[op_str][mktcap] = ror_priority_factor
            #     print(ror_prioritization_dict[op_str][mktcap])
            #     print(hits)
            #     break
    return ror_prioritization_dict

# print(optimized_prioritization_factors())
