import config, requests, json
import pandas as pd

fiveminute_bars_url = config.BARS_URL + '/5Min?symbols=MSFT&limit=1000'
daily_bars_url = '{}/day?symbols={}&limit=1000'.format(config.BARS_URL, 'MSFT,AAPL,FB,NFLX,CCJ,FVRR,AEO')
r = requests.get(daily_bars_url, headers=config.HEADERS)

data = r.json()['MSFT']
df = pd.DataFrame(data)

print(df)
