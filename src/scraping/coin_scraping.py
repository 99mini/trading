import requests
import pandas as pd
import datetime
import time
import os

def get_historical_klines(symbol, interval, start_str, end_str=None):
    base_url = 'https://api.binance.com/api/v3/klines'
    start_ts = int(datetime.datetime.strptime(start_str, '%Y-%m-%d').timestamp() * 1000)
    end_ts = None
    if end_str:
        end_ts = int(datetime.datetime.strptime(end_str, '%Y-%m-%d').timestamp() * 1000)

    klines = []
    while True:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_ts,
            'limit': 1000
        }
        if end_ts:
            params['endTime'] = end_ts

        response = requests.get(base_url, params=params)
        data = response.json()
        if not data or 'code' in data:
            break
        klines.extend(data)
        last_open_time = data[-1][0]
        if last_open_time == start_ts:
            break
        start_ts = last_open_time + 1
        if len(data) < 1000:
            break
        time.sleep(0.5)  # API rate limit 준수

    return klines

# 1년치 BTCUSDT 1일봉 데이터 수집
symbol = 'BTCUSDT'
interval = '1d'
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

klines = get_historical_klines(symbol, interval, start_date, end_date)

# DataFrame 변환
columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
           'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
           'taker_buy_quote_asset_volume', 'ignore']
df = pd.DataFrame(klines, columns=columns)

# 타임스탬프를 datetime으로 변환
for col in ['open_time', 'close_time']:
    df[col] = pd.to_datetime(df[col], unit='ms')

# 저장

root_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(root_dir, '..', 'assets', 'data', 'historical_data.csv')

df.to_csv(data_dir, index=False)

print(f"Saved {len(df)} rows of historical BTC data to {data_dir}")
