from .base_strategy import BaseStrategy

class VolatilityBreakoutStrategy(BaseStrategy):
    def __init__(self, k=0.5):
        self.k = k

    def generate_signal(self, data):
        # data: pandas DataFrame with columns ['open', 'high', 'low', 'close']
        if len(data) < 2:
            return "hold"

        prev_day = data.iloc[-2]
        today = data.iloc[-1]
        range_ = prev_day['high'] - prev_day['low']
        target = today['open'] + range_ * self.k
        if today['high'] >= target:
            return "buy"
        return "hold"
    
    def prepare_data(self, raw_data):
        df = raw_data.copy()
        df['range'] = df['high'] - df['low']
        df['target'] = df['open'] + df['range'].shift(1) * self.k
        return df.dropna()
    
    def __name__(self):
        return "VolatilityBreakoutStrategy"
