from binance.client import Client
from binance.enums import *
import os

# 환경변수 또는 직접 입력
api_key = os.getenv('BINANCE_API_KEY', 'your_api_key')
api_secret = os.getenv('BINANCE_API_SECRET', 'your_secret_key')

client = Client(api_key=api_key, api_secret=api_secret)

tickers = client.get_all_tickers()
print(type(tickers), len(tickers))
