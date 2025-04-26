from indecators import get_atr, generate_ensemble_signals

from .base_strategy import BaseStrategy

class TurtleStrategy(BaseStrategy):
    def prepare_data(self, raw_data):
        df = raw_data.copy()
        df['atr'] = get_atr(df)

        df['signal'] = generate_ensemble_signals(df, [5, 10, 20, 55, 120, 240])


    def generate_signal(self, data):
        pass


    def __name__(self):
        return "TurtleStrategy"