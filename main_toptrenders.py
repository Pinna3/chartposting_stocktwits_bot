from dailyscanner_double_agent import*

if __name__ == '__main__':
    while True:
        ###Think about another filtering mechanism (worried about shorts) (maybe restrict to long trending or winning trend, feels off)
        print_daily_counter_capacities()
        print('.')
        print('.')
        print('.')
        print('Top_Tier_Unbroken_Trenders')
        print('.')
        [print(item[0]) for item in pull_top_tier_unbroken_trenders(tier_percentage=12) if item != None]
        print('.')
        print('.')
        print('.')
        top_trender_watchlists = [penta_tuple for penta_tuple in pull_top_tier_unbroken_trenders(tier_percentage=12) if penta_tuple != None]
        for filename, timemarker, mktcap, direction, number, total in top_trender_watchlists:
            print('')
            print(filename)
            print('')
            dailyscanner_double_agent(filename, direction, publish=False)
