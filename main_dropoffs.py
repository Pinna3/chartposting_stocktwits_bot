from dailyscanner import dailyscanner

if __name__ == '__main__':
    while True:
        print('.')
        print('.')
        print('.')
        print('Dropoff Based Watchlists')
        print('.')
        [print(item[0]) for item in drop_off_based_watchlist_filter(max_per_category=3, drop_off_rate_cutoff=.25)]
        print('.')
        print('.')
        print('.')
        for filename, direction in drop_off_based_watchlist_filter(max_per_category=3, drop_off_rate_cutoff=.25):
            print('')
            print(filename)
            print('')
            dailyscanner(filename, direction, publish=False)
