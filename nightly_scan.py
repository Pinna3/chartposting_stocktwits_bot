from momoscreener import Securities, generate_list_of_time_markers
from daily_entry_optimizer import optimized_prioritization_factors

if __name__ == '__main__':
    timemarkers = generate_list_of_time_markers(80, increment=5)
    optimized_prioritization_factors_dict = optimized_prioritization_factors()

    list = Securities('StockLists/Micro<$50M.csv')
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='>', mktcap_group='Micro', ror_prioritization_factor=optimized_prioritization_factors_dict['>']['Micro'])
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='<', mktcap_group='Micro', ror_prioritization_factor=optimized_prioritization_factors_dict['<']['Micro'])

    list = Securities('StockLists/Small$50M-$300M.csv')
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='>', mktcap_group='Small', ror_prioritization_factor=optimized_prioritization_factors_dict['>']['Small'])
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='<', mktcap_group='Small', ror_prioritization_factor=optimized_prioritization_factors_dict['<']['Small'])

    list = Securities('StockLists/Medium$300M-$2B.csv')
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='>', mktcap_group='Medium', ror_prioritization_factor=optimized_prioritization_factors_dict['>']['Medium'])
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='<', mktcap_group='Medium', ror_prioritization_factor=optimized_prioritization_factors_dict['<']['Medium'])

    list = Securities('StockLists/Large$2B-$10B.csv')
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='>', mktcap_group='Large', ror_prioritization_factor=optimized_prioritization_factors_dict['>']['Large'])
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='<', mktcap_group='Large', ror_prioritization_factor=optimized_prioritization_factors_dict['<']['Large'])

    list = Securities('StockLists/VeryLarge>$10B.csv')
    # list = Securities('StockLists/verylargesample.csv')
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='>', mktcap_group='VeryLarge', ror_prioritization_factor=optimized_prioritization_factors_dict['>']['VeryLarge'])
    for timemarker in timemarkers:
        list.trend_9SMA_20SMA_50SMA_200SMA(timemarker, op_str='<', mktcap_group='VeryLarge', ror_prioritization_factor=optimized_prioritization_factors_dict['<']['VeryLarge'])
