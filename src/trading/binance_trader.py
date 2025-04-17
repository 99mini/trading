from binance.client import Client
import pandas as pd
from base import BaseTrader
import os

class BinanceTrader(BaseTrader):
    def __init__(self, strategy):
        super().__init__(strategy)
        self.client = None
    
    def _connect(self):
        self.client = Client(
            api_key=os.getenv("BINANCE_API_KEY"),
            api_secret=os.getenv("BINANCE_API_SECRET"),
            testnet=True  # 테스트넷 사용
        )
        self.connected = True
    
    def _fetch_data(self, symbol: str, interval: str) -> pd.DataFrame:
        klines = self.client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=100
        )
        return pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'trades',
            'taker_buy_base', 'taker_buy_quote', 'ignore'
        ])
    
    def _execute_order(self, symbol: str, side: str, quantity: float):
        self.client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
