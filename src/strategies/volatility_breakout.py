from .base import BaseStrategy

class VolatilityBreakoutStrategy(BaseStrategy):
    def __init__(self, k=0.5):
        self.k = k

    def generate_signal(self, data):
        # data: pandas DataFrame with columns ['open', 'high', 'low', 'close']
        prev_day = data.iloc[-2]
        today = data.iloc[-1]
        range_ = prev_day['high'] - prev_day['low']
        target = today['open'] + range_ * self.k
        if today['high'] >= target:
            return "buy"
        return "hold"
