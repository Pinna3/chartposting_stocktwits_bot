from utility_func import get_account_value
from datetime import date
today_date = date.today().strftime('%m-%d-%y')

#70% max long allocation in bull markets
def long_capacity(portfolio_current, max_exposure=69):
    return portfolio_current >= max_exposure

#30% max short allocation in bull markets
def short_capacity(portfolio_current, max_exposure=29):
    return portfolio_current >= max_exposure

#10% max allocation per industry
def industry_capacity(portfolio_current, max_exposure=9):
    return portfolio_current >= max_exposure


with open('DailyCounter.json', 'w') as outfile:
    counter = {
        'today_date': today_date,
        'long': 0,
        'long_mkt_cap': {
            'verylarge': 0,
            'large': 0,
            'medium': 0,
            'small': 0,
            'micro': 0
            }
        'short': 0,
        'short_mkt_cap': {
            'verylarge': 0,
            'large': 0,
            'medium': 0,
            'small': 0,
            'micro': 0
            }
        }
    json.dumps(counter, outfile, indent=2)
