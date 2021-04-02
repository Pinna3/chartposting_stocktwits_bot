from candlestick import SecurityTradeData
import plotly.graph_objs as go
import json
import csv
import finnhub
from time import sleep
from alpaca import get_all_positions, get_account_value, return_candles_json

def bb_param_optomizer(SecurityTradeDataObject, op_str, entry_frequency):
    candles = SecurityTradeDataObject
    def optimal_bb_window(op_str, entry_frequency):
        rolling_window_and_counter = []
        for rolling_window in range(21):
            try:
                candles.custom_bollingers(rolling_window, 1)
                rolling_window_and_counter.append([rolling_window, \
                    candles.entry_counter(op_str)])
                print(rolling_window_and_counter[rolling_window])
            except:
                continue
        for counter in rolling_window_and_counter:
            if counter[1][0] <= entry_frequency and counter[1][0] == 12:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 11:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 10:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 9:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 8:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 7:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 6:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 5:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 4:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 3:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 2:
                rolling_window = counter[0]
                return rolling_window
            elif counter[1][0] <= entry_frequency and counter[1][0] == 1:
                rolling_window = counter[0]
                return rolling_window
        return None

    def optimal_bb_std(rolling_window, op_str, entry_frequency):
        std_and_counter = []
        for index, std in enumerate([.1, .2, .3, .4, .5, .6, .7, .8, .9,
                                     1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7,
                                     1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]):
            try:
                candles.custom_bollingers(rolling_window, std)
                std_and_counter.append([std, candles.entry_counter(op_str)])
                print(std_and_counter[index])
            except:
                continue

        print('')
        for counter in std_and_counter:
            if counter[1][0] <= entry_frequency and counter[1][0] == 12:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 11:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 10:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 9:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 8:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 7:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 6:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 5:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 4:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 3:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 2:
                std = counter[0]
                return std
            elif counter[1][0] <= entry_frequency and counter[1][0] == 1:
                std = counter[0]
                return std
        return None

    bb_window = optimal_bb_window(op_str, entry_frequency)
    bb_std = optimal_bb_std(bb_window, op_str, entry_frequency)
    return bb_window, bb_std

def graph_degrees_of_trend(mktcap_dir, down_or_up_str, date_str, *time_markers):
    hits = []
    for period in time_markers:
        with open(f'{mktcap_dir}Stocks/Watchlists/03-30-21/({period},)D-4E-{down_or_up_str}trend{date_str}.json') as infile:
            list = json.load(infile)
            hits.append(len(list))
            print(period, len(list))
    trace = {'x': time_markers, 'y': hits, 'type': 'scatter', 'mode': 'lines',
        'line': {'width': 1, 'color': 'blue'}, 'name': 'Hits'}
    data = [trace]
    layout = go.Layout({'title': {'text': f'{mktcap_dir} {down_or_up_str}trend Hits',
            'font': {'size': 15}}})
    fig = go.Figure(data=data, layout=layout)
    fig.show()

def calculate_and_file_dropoff_rates(mktcap_dir, down_or_up_str, date_str, *time_markers, interval=5):
    hits = []
    for period in time_markers:
        with open(f'{mktcap_dir}Stocks/Watchlists/03-30-21/({period},)D-4E-{down_or_up_str}trend{date_str}.json') as infile:
            list = json.load(infile)
            hits.append(len(list))
            # print(period, len(list))
    dropoffs = []
    for index, count in enumerate(hits):
        if index != 0:
            try:
                dropoff = round(1 - (count / hits[index-1]), 2)
                dropoffs.append((index * interval, dropoff, count, hits[0], round(count/hits[0], 3)))
            except ZeroDivisionError:
                dropoff = 0
                dropoffs.append((index * interval, dropoff, count, hits[0], round(count/hits[0], 3)))
    dropoffs_sorted = sorted(dropoffs, key = lambda x: x[1])
    with open(f'{mktcap_dir}Stocks/WeeklyDropOff/{down_or_up_str}trend{date_str}.json', 'w') as outfile:
        json.dump((dropoffs, dropoffs_sorted), outfile, indent=4)
    return dropoffs, dropoffs_sorted

def count_stock_csv_list(csv_source):
    securities = []
    # CSV Database- comprehensive list of optionable stocks obtain from barchart
    with open(csv_source, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)  # skip the header line
        for row in reader:
            ticker = str(row[0])
            securities.append(ticker)
    return(len(securities))

def return_list_of_tickers(csv_source):
    securities = []
    # CSV Database- comprehensive list of optionable stocks obtain from barchart
    with open(csv_source, 'r') as infile:
        reader = csv.reader(infile)
        next(reader)  # skip the header line
        for row in reader:
            ticker = str(row[0])
            securities.append(ticker)
    return securities

#experiment with prioritizing methods... right now leaning towards ranking_time_weighted_sorted
#mktcap_group = 'VeryLarge', 'Large', 'Medium', 'Small', 'Micro'
#trend = 'up', 'down'
#date = 'MM-DD-YY'
#*time_markers = 1, 5, 10, 15, 20, 25, ... etc
#interval = time between time_markers
def rank_dropoffs(mktcap_group, trend, date, *time_markers, interval=5):
    graph_degrees_of_trend(mktcap_group, trend, date, *time_markers)
    dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates(mktcap_group, trend, date, *time_markers, interval)
    ranking = []
    ranking_time_weighted = []
    # print('')
    # print(dropoffs)
    # print('')
    for tuple in dropoffs_sorted:
        days, dropoff_rate, count, starting_total, percentage_of_total = tuple
        try:
            rating = round(percentage_of_total / dropoff_rate, 2)
        except ZeroDivisionError:
            rating = 0
        ranking.append((days, rating))
        weighted_ranking = round(days * rating, 2)
        ranking_time_weighted.append((days, weighted_ranking))
    ranking_sorted = sorted(ranking, key = lambda x: x[1], reverse=True)
    ranking_time_weighted_sorted = sorted(ranking_time_weighted, key = lambda x: x[1], reverse=True)
    # print(ranking_sorted)
    print(ranking_time_weighted_sorted)
    print('')


def initialize_holdings():
    positions = get_all_positions()
    holdings = {
        "long": {
            "market_value": None,
            "acct_percentage": None,
            "industry": {
            }
        },
        "short": {
            "market_value": None,
            "acct_percentage": None,
            "industry": {
            }
        },
    }
    for holding in positions:
        symbol = holding['symbol']
        market_value = round(float(holding['market_value']), 2)
        side = holding['side']
        finnhub_client = finnhub.Client(api_key='c1aiaan48v6v5v4gv69g')
        try:
            industry = finnhub_client.company_profile2(symbol=symbol)['finnhubIndustry']
        except KeyError:
            industry = 'ETF'
        sleep(1)
        if industry not in holdings[side]['industry'].keys():
            holdings[side]['industry'][industry] = {}
            holdings[side]['industry'][industry]['market_value'] = None
            holdings[side]['industry'][industry]['acct_percentage'] = None
            holdings[side]['industry'][industry]['stocks'] = [[symbol, market_value]]
        else:
            holdings[side]['industry'][industry]['stocks'].append([symbol, market_value])

    acct_value = get_account_value()
    long_industry_keys = holdings['long']['industry'].keys()
    short_industry_keys = holdings['short']['industry'].keys()
    for industry in long_industry_keys:
        market_value = 0.0
        for stock in holdings['long']['industry'][industry]['stocks']:
            market_value += round(float(stock[1]), 2)
        holdings['long']['industry'][industry]['market_value'] = market_value
        holdings['long']['industry'][industry]['acct_percentage'] = round((market_value / acct_value) * 100, 2)
    for industry in short_industry_keys:
        market_value = 0.0
        for stock in holdings['short']['industry'][industry]['stocks']:
            market_value += round(float(stock[1]), 2)
        holdings['short']['industry'][industry]['market_value'] = market_value
        holdings['short']['industry'][industry]['acct_percentage'] = round((market_value / acct_value) * 100, 2)

    long_market_value = 0.0
    for industry in long_industry_keys:
        long_market_value += round(holdings['long']['industry'][industry]['market_value'], 2)
    holdings['long']['market_value'] = round(long_market_value, 2)
    holdings['long']['acct_percentage'] = round((long_market_value / acct_value) * 100, 2)
    short_market_value = 0.0
    for industry in short_industry_keys:
        short_market_value += round(holdings['short']['industry'][industry]['market_value'], 2)
    holdings['short']['market_value'] = round(short_market_value, 2)
    holdings['short']['acct_percentage'] = round((short_market_value / acct_value) * 100, 2)

    return holdings

def tag_imported_stock_csv_file_with_smoothness_test(csv_in, csv_out):
    with open(csv_in) as infile:
        reader = csv.reader(infile)
        next(reader)

        processed_data = []
        for row in reader:
            stock = row[0]
            smoothness_test = True
            data = return_candles_json(stock, period='day', num_bars=365)
            for index, ohlc in enumerate(data[stock][:-1]):
                if abs(float(ohlc['c']) - float(data[stock][index+1]['o'])) > (float(ohlc['c']) * .5):
                    smoothness_test = False
            row.append(smoothness_test)
            processed_data.append(row)
            sleep(.3)
            print(row)

        with open(csv_out, 'w') as outfile:
            writer = csv.writer(outfile)
            for row in processed_data:
                writer.writerow(row)









# graph_degrees_of_trend('Small', 'up', '03-30-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80)
# calculate_and_file_dropoff_rates('Small', 'up', '03-30-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# rank_dropoffs('Small', 'up', '03-30-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# rank_dropoffs('Large', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# rank_dropoffs('Medium', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# rank_dropoffs('Small', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# rank_dropoffs('Micro', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)

# graph_degrees_of_trend('VeryLarge', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('VeryLarge', 'down', '03-29-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# print(dropoffs_sorted)

# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('VeryLarge', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# for instance in dropoffs_sorted:
#     index, drop_off_rate, count, total, count_total_fract = instance
#     if drop_off_rate != 0 and count_total_fract > .3 and drop_off_rate < .3:
#         print('VeryLarge')
#         print(instance)
# print('')
# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('Large', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# for instance in dropoffs_sorted:
#     index, drop_off_rate, count, total, count_total_fract = instance
#     if drop_off_rate != 0 and count_total_fract > .3 and drop_off_rate < .3:
#         print('Large')
#         print(instance)
# print('')
# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('Medium', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# for instance in dropoffs_sorted:
#     index, drop_off_rate, count, total, count_total_fract = instance
#     if drop_off_rate != 0 and count_total_fract > .3 and drop_off_rate < .3:
#         print('Medium')
#         print(instance)
# print('')
# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('Small', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# for instance in dropoffs_sorted:
#     index, drop_off_rate, count, total, count_total_fract = instance
#     if drop_off_rate != 0 and count_total_fract > .3 and drop_off_rate < .3:
#         print('Small')
#         print(instance)
# print('')
# dropoffs, dropoffs_sorted = calculate_and_file_dropoff_rates('Micro', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# for instance in dropoffs_sorted:
#     index, drop_off_rate, count, total, count_total_fract = instance
#     if drop_off_rate != 0 and count_total_fract > .3 and drop_off_rate < .3:
#         print('Micro')
#         print(instance)
