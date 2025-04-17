import pandas as pd

from .base_strategy import BaseStrategy

class MovingAverageStrategy(BaseStrategy):
    def prepare_data(self, raw_data):
        df = raw_data.copy()
        df['MA20'] = df['close'].rolling(20).mean()
        df['MA50'] = df['close'].rolling(50).mean()
        return df.dropna()
    
    def generate_signal(self, data):
        latest = data.iloc[-1]
        if latest['MA20'] > latest['MA50']:
            return "buy"
        return "sell"
