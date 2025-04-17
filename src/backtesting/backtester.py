import pandas as pd
from typing import Type
from strategies.base import BaseStrategy

class Backtester:
    def __init__(self, strategy: Type[BaseStrategy]):
        self.strategy = strategy()
        self.historical_data = None
    
    def load_data(self, data_path: str):
        self.historical_data = pd.read_csv(data_path)
    
    def run(self) -> dict:
        processed_data = self.strategy.prepare_data(self.historical_data)
        signals = []
        returns = []
        
        for i in range(1, len(processed_data)):
            window = processed_data.iloc[:i]
            signal = self.strategy.generate_signal(window)
            signals.append(signal)
            
            # 수익률 계산 로직 (예시)
            if signal == "buy":
                returns.append(processed_data['close'][i] - processed_data['open'][i])
        
        return {
            "signals": signals,
            "returns": returns,
            "sharpe_ratio": self._calculate_sharpe(returns),
            "max_drawdown": self._calculate_max_drawdown(returns)
        }
    
    def _calculate_sharpe(self, returns):
        # 샤프지수 계산 구현
        
        pass
