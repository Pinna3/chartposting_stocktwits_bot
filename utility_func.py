from candlestick import SecurityTradeData
import plotly.graph_objs as go
import json
import csv

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

def graph_degrees_of_trend(mktcap_dir, down_or_up_str, date_str, *time_markers, interval=5):
    hits = []
    for period in time_markers:
        with open(f'{mktcap_dir}Stocks/({period},)D-{down_or_up_str}trend{date_str}.json') as infile:
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
        with open(f'{mktcap_dir}Stocks/({period},)D-{down_or_up_str}trend{date_str}.json') as infile:
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


# graph_degrees_of_trend('VeryLarge', 'up', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# calculate_and_file_dropoff_rates('VeryLarge', 'up', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# graph_degrees_of_trend('VeryLarge', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
# calculate_and_file_dropoff_rates('VeryLarge', 'down', '03-28-21', 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, interval=5)
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
