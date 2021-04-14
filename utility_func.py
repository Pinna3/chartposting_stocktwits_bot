from candlestick import SecurityTradeData, pandas_atr_calculation
import plotly.graph_objs as go
import json
import csv
import finnhub
from time import sleep
from alpaca import get_all_positions, get_account_value, return_candles_json, get_all_portfolio_tickers
from risk_parameter import open_mktcap_capacities_dict, open_sector_capacities_dict
import pandas as pd
from glob import glob
from datetime import datetime, date
today_date = date.today().strftime('%m-%d-%y')

###Check for proper ranges using get_bb_params_distribution(), last window=2-20 = (range(2, 21)), last std=.1-1 (4/6/21), expand for testing once in a while
def bb_param_optomizer_WITH_average(SecurityTradeDataObject, op_str, entry_frequency, timebar,
                       window_range=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                       std_range=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]):
    candles = SecurityTradeDataObject
    def optimal_bb_window(op_str, entry_frequency, timebar):
        rolling_window_and_counter = []
        for index, rolling_window in enumerate(window_range):
            # try:
                candles.custom_bollingers(rolling_window, 1)
                rolling_window_and_counter.append([rolling_window, \
                    candles.entry_counter_bollingers_WITH_average(op_str, timebar)])
                # print(rolling_window_and_counter[index])
            # except:
            #     continue
        ###update range according to get_bb_params_distribution()
        entry_frequency_range = sorted([x for x in range(1,entry_frequency + 1)], reverse=True)
        for counter in rolling_window_and_counter:
            for entries in entry_frequency_range:
                if counter[1][0] <= entry_frequency and counter[1][0] == entries:
                    rolling_window = counter[0]
                    return rolling_window
        return None

    def optimal_bb_std(rolling_window, op_str, entry_frequency, timebar):
        std_and_counter = []
        for index, std in enumerate(std_range):
            try:
                candles.custom_bollingers(rolling_window, std)
                std_and_counter.append([std, candles.entry_counter_bollingers_WITH_average(op_str, timebar)])
                # print(std_and_counter[index])
            except:
                continue
        # print('')
        entry_frequency_range = sorted([x for x in range(1,entry_frequency + 1)], reverse=True)
        for counter in std_and_counter:
            for entries in entry_frequency_range:
                if counter[1][0] <= entry_frequency and counter[1][0] == entries:
                    std = counter[0]
                    return std
        return None
    bb_window = optimal_bb_window(op_str, entry_frequency, timebar)
    bb_std = optimal_bb_std(bb_window, op_str, entry_frequency, timebar)
    return bb_window, bb_std

def bb_param_optomizer_WITHOUT_average(SecurityTradeDataObject, op_str, entry_frequency, timebar,
                       window_range=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                       std_range=[.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]):
    candles = SecurityTradeDataObject
    def optimal_bb_window(op_str, entry_frequency, timebar):
        rolling_window_and_counter = []
        for index, rolling_window in enumerate(window_range):
            try:
                candles.custom_bollingers(rolling_window, 1)
                rolling_window_and_counter.append([rolling_window, \
                    candles.entry_counter_bollingers_WITHOUT_average(op_str, timebar)])
                # print(rolling_window_and_counter[index])
            except:
                continue
        ###update range according to get_bb_params_distribution()
        entry_frequency_range = sorted([x for x in range(1,entry_frequency + 1)], reverse=True)
        for counter in rolling_window_and_counter:
            for entries in entry_frequency_range:
                if counter[1] <= entry_frequency and counter[1] == entries:
                    rolling_window = counter[0]
                    return rolling_window
        return None

    def optimal_bb_std(rolling_window, op_str, entry_frequency, timebar):
        std_and_counter = []
        for index, std in enumerate(std_range):
            try:
                candles.custom_bollingers(rolling_window, std)
                std_and_counter.append([std, candles.entry_counter_bollingers_WITHOUT_average(op_str, timebar)])
                # print(std_and_counter[index])
            except:
                continue
        # print('')
        entry_frequency_range = sorted([x for x in range(1,entry_frequency + 1)], reverse=True)
        for counter in std_and_counter:
            for entries in entry_frequency_range:
                if counter[1] <= entry_frequency and counter[1] == entries:
                    std = counter[0]
                    return std
        return None
    bb_window = optimal_bb_window(op_str, entry_frequency, timebar)
    bb_std = optimal_bb_std(bb_window, op_str, entry_frequency, timebar)
    return bb_window, bb_std

def sm200doubleagent_window_optomizer_WITHOUT_average(SecurityTradeDataObject, op_str, entry_frequency, timebar,
                       window_range=range(2, 201)):
    candles = SecurityTradeDataObject
    window_and_counter = []
    for index, window in enumerate(window_range):
        # try:
        candles.sma200_double_agent_activate(window)
        window_and_counter.append([window, candles.entry_counter_200sma_double_agent_WITHOUT_average(op_str, timebar)])
        # except:
        #     continue
    entry_frequency_range = sorted([x for x in range(1, entry_frequency + 1)], reverse=True)
    for counter in window_and_counter:
        for entries in entry_frequency_range:
            if counter[1] <= entry_frequency and counter[1] <= entries:
                window = counter[0]
                candles.sma200_double_agent_activate(200)
                return window
    candles.sma200_double_agent_activate(200)
    return None

def generate_list_of_time_markers(title_time_marker, increment=5):
    head_timebar = title_time_marker
    initial_timebar = [1]
    [initial_timebar.append(timebar*increment) for timebar in range(1, int(head_timebar/increment+1))]
    return initial_timebar

def graph_degrees_of_trend(mktcap_dir, down_or_up_str, title_time_marker):
    hits = []
    time_markers = generate_list_of_time_markers(title_time_marker)
    for period in time_markers:
        with open(f'{mktcap_dir}Stocks/Watchlists/[{period}]D-{down_or_up_str}trend.json') as infile:
            list = json.load(infile)
            hits.append(len(list))
            # print(period, len(list))
    trace = {'x': time_markers, 'y': hits, 'type': 'scatter', 'mode': 'lines',
        'line': {'width': 1, 'color': 'blue'}, 'name': 'Hits'}
    data = [trace]
    layout = go.Layout({'title': {'text': f'{mktcap_dir} {down_or_up_str}trend Hits',
            'font': {'size': 15}}})
    fig = go.Figure(data=data, layout=layout)
    fig.show()
    return f'{mktcap_dir} {down_or_up_str}trend'

def calculate_and_file_dropoff_rates(mktcap_dir, down_or_up_str, title_time_marker, interval=5):
    hits = []
    time_markers = generate_list_of_time_markers(title_time_marker)
    for period in time_markers:
        with open(f'{mktcap_dir}Stocks/Watchlists/[{period}]D-{down_or_up_str}trend.json') as infile:
            list = json.load(infile)
            hits.append(len(list))
    dropoffs = []
    date = today_date
    for index, count in enumerate(hits):
        if index != 0:
            try:
                dropoff = round(1 - (count / hits[index-1]), 2)
                percentage = round(count/hits[0], 3)
                dropoffs.append((index * interval, dropoff, count, hits[0], percentage))
            except ZeroDivisionError:
                try:
                    dropoff = 0
                    percentage = round(count/hits[0], 3)
                    dropoffs.append((index * interval, dropoff, count, hits[0], percentage))
                except ZeroDivisionError:
                    dropoff = 0
                    percentage = 0
                    dropoffs.append((index * interval, dropoff, count, hits[0], percentage))
    dropoffs_sorted = sorted(dropoffs, key = lambda x: x[1])
    csv_row = [date]
    for group in dropoffs_sorted:
        if group[1] <= 0:
            continue
        else:
            for datapoint in group:
                csv_row.append(datapoint)
    with open(f'{mktcap_dir}Stocks/WeeklyDropOff/{down_or_up_str}trend.csv') as infile:
        reader = csv.reader(infile)
        up_to_date = False
        for row in reader:
            if row[0] == date:
                up_to_date = True
        if up_to_date == False:
            with open(f'{mktcap_dir}Stocks/WeeklyDropOff/{down_or_up_str}trend.csv', 'a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(csv_row)
    return dropoffs_sorted

#experiment with prioritizing methods... right now using ranking_time_weighted_sorted
#mktcap_group = 'VeryLarge', 'Large', 'Medium', 'Small', 'Micro'
#trend = 'up', 'down'
#*time_markers = 1, 5, 10, 15, 20, 25, ... etc
#interval = time between time_markers
def rank_dropoffs(mktcap_group, trend, title_time_marker, interval=5):
    dropoffs_s = calculate_and_file_dropoff_rates(mktcap_group, trend, title_time_marker, interval)
    ranking = []
    ranking_time_weighted = []
    for tuple in dropoffs_s:
        days, dropoff_rate, count, starting_total, percentage_of_total = tuple
        try:
            rating = round(percentage_of_total / dropoff_rate, 2)
        except ZeroDivisionError:
            rating = 0
        if days != 5:
            starting = days - 5
        else:
            starting = 1
        ranking.append({'days': days, 'starting': starting, 'drop_rate': dropoff_rate, 'percentage': percentage_of_total, 'quality_rating': rating})
        weighted_rating = round(days * rating, 2)
        ranking_time_weighted.append({'days': days, 'starting': starting, 'drop_rate': dropoff_rate, 'percentage': percentage_of_total, 'quality_rating': weighted_rating})
    drop_off_percentage_sorted = sorted(ranking, key = lambda x: x['drop_rate'], reverse=False)
    ranking_sorted = sorted(ranking, key = lambda x: x['quality_rating'], reverse=True)
    ranking_time_weighted_sorted = sorted(ranking_time_weighted, key = lambda x: x['quality_rating'], reverse=True)
    return [[dict['starting'], dict['drop_rate']] for dict in ranking_time_weighted_sorted]

def fetch_sector(symbol):
    files = ['Micro<$50M', 'Small$50M-$300M', 'Medium$300M-$2B', 'Large$2B-$10B', 'VeryLarge>$10B']
    for file in files:
        with open(f'StockLists/{file}.csv') as infile:
            reader = csv.reader(infile)
            next(reader)
            for row in reader:
                if row[0] == symbol:
                    return row[8]

def initialize_sector_allocation_dict():
    positions = get_all_positions()
    sector_allocation_dict = {
        "long": {
            "market_value": None,
            "acct_percentage": None,
            "sector": {
            }
        },
        "short": {
            "market_value": None,
            "acct_percentage": None,
            "sector": {
            }
        },
    }
    for holding in positions:
        symbol = holding['symbol']
        market_value = abs(round(float(holding['market_value']), 2))
        side = holding['side']
        sector = fetch_sector(symbol)
        if sector not in sector_allocation_dict[side]['sector'].keys():
            sector_allocation_dict[side]['sector'][sector] = {}
            sector_allocation_dict[side]['sector'][sector]['market_value'] = None
            sector_allocation_dict[side]['sector'][sector]['acct_percentage'] = None
            sector_allocation_dict[side]['sector'][sector]['stocks'] = [[symbol, market_value]]
        else:
            sector_allocation_dict[side]['sector'][sector]['stocks'].append([symbol, market_value])

    acct_value = get_account_value()
    long_sector_keys = sector_allocation_dict['long']['sector'].keys()
    short_sector_keys = sector_allocation_dict['short']['sector'].keys()
    for sector in long_sector_keys:
        market_value = 0.0
        for stock in sector_allocation_dict['long']['sector'][sector]['stocks']:
            market_value += round(float(stock[1]), 2)
        sector_allocation_dict['long']['sector'][sector]['market_value'] = market_value
        sector_allocation_dict['long']['sector'][sector]['acct_percentage'] = round((market_value / acct_value) * 100, 2)
    for sector in short_sector_keys:
        market_value = 0.0
        for stock in sector_allocation_dict['short']['sector'][sector]['stocks']:
            market_value += round(float(stock[1]), 2)
        sector_allocation_dict['short']['sector'][sector]['market_value'] = market_value
        sector_allocation_dict['short']['sector'][sector]['acct_percentage'] = round((market_value / acct_value) * 100, 2)

    long_market_value = 0.0
    for sector in long_sector_keys:
        long_market_value += round(sector_allocation_dict['long']['sector'][sector]['market_value'], 2)
    sector_allocation_dict['long']['market_value'] = round(long_market_value, 2)
    sector_allocation_dict['long']['acct_percentage'] = round((long_market_value / acct_value) * 100, 2)
    short_market_value = 0.0
    for sector in short_sector_keys:
        short_market_value += round(sector_allocation_dict['short']['sector'][sector]['market_value'], 2)
    sector_allocation_dict['short']['market_value'] = round(short_market_value, 2)
    sector_allocation_dict['short']['acct_percentage'] = round((short_market_value / acct_value) * 100, 2)

    with open('SectorAllocationDict.json', 'w') as outfile:
        json.dump(sector_allocation_dict, outfile, indent=2)
    return sector_allocation_dict

def tag_imported_stock_csv_file_with_smoothness_test(csv_in, csv_out):
    with open(csv_in) as infile:
        reader = csv.reader(infile)
        next(reader)
        processed_data = []
        for row in reader:
            stock = row[0]
            smoothness_test = True
            data = return_candles_json(stock, period_len='day', num_bars=365)
            for index, ohlc in enumerate(data[stock][:-1]):
                if abs(float(ohlc['c']) - float(data[stock][index+1]['o'])) > (float(ohlc['c']) * .5):
                    smoothness_test = False
            row.append(smoothness_test)
            processed_data.append(row)
            sleep(.3)
        with open(csv_out, 'w') as outfile:
            writer = csv.writer(outfile)
            for row in processed_data:
                writer.writerow(row)

def tag_imported_stock_csv_file_with_peers(csv_in, csv_out):
    finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
    with open(csv_in) as infile:
        reader = csv.reader(infile)
        next(reader)
        processed_data = []
        for row in reader:
            peers = None
            while peers is None:
                try:
                    peers = finnhub_client.company_peers(row[0])
                    sleep(1.1)
                except:
                    continue
            hashable_peers = []
            for peer in peers:
                hashable_peer = '$' + peer
                hashable_peers.append(hashable_peer)
            peer_group = hashable_peers[0:3]
            peer_group.append('$SPY')
            #Solves ETF lack of peers issue for publishing purposes
            if len(peer_group) <= 1:
                peer_group.append('$DIA')
                peer_group.append('$IWM')
                peer_group.append('$QQQ')
            row.append(' '.join(peer_group).strip())
            processed_data.append(row)
        with open(csv_out, 'w') as outfile:
            writer = csv.writer(outfile)
            for row in processed_data:
                writer.writerow(row)

def make_pulled_csv_list_consumable(csv_in, atr_rolling_window=14):
    with open(csv_in) as infile:
        stocks = infile.readlines()
    symbols = [stock.split(',')[0].strip() for stock in stocks[1:]]
    mkt_caps = [stock.split(',')[5].strip() for stock in stocks[1:]]
    sectors = [stock.split(',')[8].strip() for stock in stocks[1:]]
    smoothness_tests = [stock.split(',')[10].strip() for stock in stocks[1:]]
    peers = [stock.split(',')[11].strip() for stock in stocks[1:]]
    sma200_double_agent = None
    #15 allows us to handle up to 3000 stocks without complications
    batch = len(symbols) // 15
    remainder = len(symbols) % 15
    #remainder batch dataframe conversion
    remainder_reference = symbols[-remainder:]
    remainder_mkt_cap = mkt_caps[-remainder:]
    remainder_sector = sectors[-remainder:]
    remainder_smoothness_test = smoothness_tests[-remainder:]
    remainder_peers = peers[-remainder:]
    # remainder_sma200_double_agent = [None for sma200_double_agent in range(remainder)]
    remainder_batch = ','.join(remainder_reference)
    remainder_data = return_candles_json(remainder_batch, period_len='day', num_bars=281)
    #iterable list with retrievable values
    remainder_df_list = []
    for index, reference_symbol in enumerate(remainder_reference):
        df = pd.DataFrame(remainder_data[reference_symbol])
        del df['t']
        sma9 = round(df.c.rolling(window=9, min_periods=9).mean(), 2)
        sma20 = round(df.c.rolling(window=20, min_periods=20).mean(), 2)
        sma50 = round(df.c.rolling(window=50, min_periods=50).mean(), 2)
        sma200 = round(df.c.rolling(window=200, min_periods=200).mean(), 2)
        df['sma9'] = sma9
        df['sma20'] = sma20
        df['sma50'] = sma50
        df['sma200'] = sma200
        #### standard  2 and 20 bollinger data
        bollinger_reference_lower = df.l.rolling(window=20, min_periods=20).mean()
        bollinger_reference_upper = df.h.rolling(window=20, min_periods=20).mean()
        sigma_lower = df.l.rolling(window=20, min_periods=20).std()
        sigma_upper = df.h.rolling(window=20, min_periods=20).std()
        df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
        df['upper'] = bollinger_reference_upper + (2 * sigma_upper)
        df['atr'] = pandas_atr_calculation(df, atr_rolling_window)
        remainder_df_list.append([reference_symbol, remainder_mkt_cap[index], remainder_sector[index], remainder_smoothness_test[index], remainder_peers[index], sma200_double_agent, df])
    total_batch_df_list = []
    for batch_num in range(1, 16):
        symbol_reference = symbols[(batch_num - 1)*batch: batch_num*batch]
        batch_mkt_cap = mkt_caps[(batch_num - 1)*batch: batch_num*batch]
        batch_sector = sectors[(batch_num - 1)*batch: batch_num*batch]
        batch_smoothness_test = smoothness_tests[(batch_num - 1)*batch: batch_num*batch]
        batch_peers = peers[(batch_num - 1)*batch: batch_num*batch]
        # batch_sma200_double_agent = [None for sma200_double_agent in range(batch)]
        symbol_batch = ','.join(symbol_reference)
        batch_data = return_candles_json(symbol_batch, period_len='day', num_bars=281)
        #iterable list with retrievable values
        batch_df_list = []
        for index, reference_symbol in enumerate(symbol_reference):
            df = pd.DataFrame(batch_data[reference_symbol])
            del df['t']
            sma9 = round(df.c.rolling(window=9, min_periods=9).mean(), 2)
            sma20 = round(df.c.rolling(window=20, min_periods=20).mean(), 2)
            sma50 = round(df.c.rolling(window=50, min_periods=50).mean(), 2)
            sma200 = round(df.c.rolling(window=200, min_periods=200).mean(), 2)
            df['sma9'] = sma9
            df['sma20'] = sma20
            df['sma50'] = sma50
            df['sma200'] = sma200
            #### standard  2 and 20 bollinger data
            bollinger_reference_lower = df.l.rolling(window=20, min_periods=20).mean()
            bollinger_reference_upper = df.h.rolling(window=20, min_periods=20).mean()
            sigma_lower = df.l.rolling(window=20, min_periods=20).std()
            sigma_upper = df.h.rolling(window=20, min_periods=20).std()
            df['lower'] = bollinger_reference_lower - (2 * sigma_lower)
            df['upper'] = bollinger_reference_upper + (2 * sigma_upper)
            df['atr'] = pandas_atr_calculation(df, atr_rolling_window)
            batch_df_list.append([reference_symbol, batch_mkt_cap[index], batch_sector[index], batch_smoothness_test[index], batch_peers[index], sma200_double_agent, df])
        for item in batch_df_list:
            if item not in total_batch_df_list:
                total_batch_df_list.append(item)
        for item in remainder_df_list:
            if item not in total_batch_df_list:
                total_batch_df_list.append(item)
    return total_batch_df_list

def drop_off_based_watchlist_filter(max_per_category=3, drop_off_rate_cutoff=.25):
    approved_files_w_operator = []
    for direction in ['up', 'down']:
        for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
            if direction == 'up':
                operator = '>'
            elif direction == 'down':
                operator = '<'
            time_weighted_ranked = rank_dropoffs(mktcap, direction, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
            for result in time_weighted_ranked[:max_per_category]:
                if result[1] < drop_off_rate_cutoff:
                    approved_files_w_operator.append([f'{mktcap}Stocks/Watchlists/({result[0]},)D-{direction}trend.json', operator])
    return approved_files_w_operator

def extract_time_marker_from_filename(filename):
    filename_str = filename
    char_list = [char for char in filename_str]
    num_list = [num for num in char_list if num.isdigit()]
    time_marker = int(''.join(num_list))
    return time_marker

def pull_top_tier_unbroken_trenders(tier_percentage=15):
    def there_can_only_be_n(watchlists, tier_percentage, op_str):
        grandtotal = watchlists[0][0]
        for total, file in watchlists:
            if total < (tier_percentage / 100) * grandtotal and total != 0:
                return [file, extract_time_marker_from_filename(file), group, op_str, total, grandtotal]
    top_trenders = {}
    top_tier_list = []
    mkt_caps = ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']
    for group in mkt_caps:
        top_trenders[group] = []
        for file in glob(f'{group}Stocks/Watchlists/*uptrend.json'):
            with open(file) as infile:
                content = json.load(infile)
                top_trenders[group].append([len(content), file])
                top_trenders[group].sort(reverse=True)
        top_tier_list.append(there_can_only_be_n(top_trenders[group], tier_percentage, '>'))
    for group in mkt_caps:
        top_trenders[group] = []
        for file in glob(f'{group}Stocks/Watchlists/*downtrend.json'):
            with open(file) as infile:
                content = json.load(infile)
                top_trenders[group].append([len(content), file])
                top_trenders[group].sort(reverse=True)
        top_tier_list.append(there_can_only_be_n(top_trenders[group], tier_percentage, '<'))
    return top_tier_list
# print(pull_top_tier_unbroken_trenders(tier_percentage=15))
#returns bb_params for all trending symbols (window and std) as a set for use in bb_param_optomizer
#range settings.
def get_bb_params_distribution():
    param_count = {'bb_window': [], 'bb_std': []}
    for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
        for file in glob(f'{mktcap}Stocks/Watchlists/*.json'):
            with open(file) as infile:
                watchlist = json.load(infile)
                for item in watchlist:
                    bb_window = item['bb_window']
                    bb_std = item['bb_std']
                    param_count['bb_window'].append(bb_window)
                    param_count['bb_std'].append(bb_std)
    bb_windows = param_count['bb_window']
    bb_stds = param_count['bb_std']
    bb_window_dist = sorted(set([x for x in bb_windows if x != None]), reverse=True)
    bb_stds_dist = sorted(set(x for x in bb_stds if x != None), reverse=True)
    return bb_window_dist, bb_stds_dist

def yield_first_nonzero_dropoff_tuple_below_threshold(mktcap_dir, down_or_up_str, title_time_marker, interval=5, threshold=.25):
    for tuple in calculate_and_file_dropoff_rates(mktcap_dir, down_or_up_str, title_time_marker):
        if tuple[1] != 0 and tuple[1] <= threshold:
            return tuple

def get_initializer_stocks_dictionary():
    open_mktcap_capacities = open_mktcap_capacities_dict()
    open_sector_capacities = open_sector_capacities_dict()
    current_portfolio = get_all_portfolio_tickers()
    initializer_list_dict = {
        '>': {
            'VeryLarge': [],
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
    #buying the dropoffs at the tail end under the logic that the low dropoff rate will continue for the next period, i.e. strong stock basket
    for direction in ['up', 'down']:
        for mktcap in ['VeryLarge', 'Large', 'Medium', 'Small', 'Micro']:
            with open(f"{mktcap}Stocks/Watchlists/[{yield_first_nonzero_dropoff_tuple_below_threshold(mktcap, direction, 80, interval=5)[0]}]D-{direction}trend.json") as infile:
                watchlist = json.load(infile)
                if direction == 'up':
                    op_str = '>'
                elif direction == 'down':
                    op_str = '<'
                for stock in watchlist:
                    if stock['ticker'] not in current_portfolio and open_sector_capacities[op_str][stock['sector']] > 0 and open_mktcap_capacities[op_str][mktcap] > 0:
                        initializer_list_dict[op_str][mktcap].append(stock['ticker'])
                        open_mktcap_capacities[op_str][mktcap] -= 1
                        open_sector_capacities[op_str][stock['sector']] -= 1

    return initializer_list_dict




# print(get_initializer_stocks_dictionary())
