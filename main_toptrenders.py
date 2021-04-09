from dailyscanner import dailyscanner

if __name__ == '__main__':
    while True:
        ###Think about another filtering mechanism (worried about shorts) (maybe restrict to long trending or winning trend, feels off)
        print('.')
        print('.')
        print('.')
        print('Top_Tier_Unbroken_Trenders')
        print('.')
        [print(item[0]) for item in pull_top_tier_unbroken_trenders(tier_percentage=10)]
        print('.')
        print('.')
        print('.')
        for filename, direction, number, total in pull_top_tier_unbroken_trenders(tier_percentage=10):
            print('')
            print(filename)
            print('')
            dailyscanner(filename, direction, publish=False)
