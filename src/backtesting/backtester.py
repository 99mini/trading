import pandas as pd
from typing import Type

from strategies import BaseStrategy

class Backtester:
    def __init__(self, strategy_cls: Type[BaseStrategy]):
        self.strategy = strategy_cls()
        self.historical_data = None
    
    def load_data(self, data_path: str):
        self.historical_data = pd.read_csv(data_path)
    
    def run(self) -> dict:
        """
        @param self:
        """
        processed_data = self.strategy.prepare_data(self.historical_data)
        signals = []
        returns = []
        
        for i in range(1, len(processed_data)):
            window = processed_data.iloc[:i]
            signal = self.strategy.generate_signal(window)
            signals.append(signal)
            
            # 수익률 계산 로직 (예시)
            if signal == "buy":
                returns.append(processed_data['close'].iloc[i] - processed_data['open'].iloc[i])
            elif signal == "sell":
                returns.append(processed_data['open'].iloc[i] - processed_data['close'].iloc[i])
            else:
                returns.append(0)
        
        return {
            "signals": signals,
            "returns": returns,
            "sharpe_ratio": self._calculate_sharpe(returns),
            "max_drawdown": self._calculate_max_drawdown(returns),
            "duration": [self.historical_data['open_time'].loc[0], self.historical_data['open_time'].loc[len(self.historical_data) - 1]],
            "total_trades": len([s for s in signals if s == "buy"]),
            "win_rate": len([r for r in returns if r > 0]) / len(returns) * 100,
            "total_return": sum(returns),
        }
    
    def _calculate_sharpe(self, returns):
        """
        Sharpe ratio

        sharpe_ratio = (mean_return - risk_free_rate) / std_dev
        """
        
        if len(returns) == 0:
            return 0
        
        mean_return = sum(returns) / len(returns)
        risk_free_rate = 0.01
        excess_returns = [r - risk_free_rate for r in returns]
        std_dev = (sum((r - mean_return) ** 2 for r in excess_returns) / len(excess_returns)) ** 0.5
        if std_dev == 0:
            return 0
        return mean_return / std_dev if std_dev != 0 else 0

    def _calculate_max_drawdown(self, returns):
        """
        max drawdown
        """

        if len(returns) == 0:
            return 0
        max_drawdown = 0
        peak = returns[0]
        for r in returns:
            if r > peak:
                peak = r
            drawdown = (peak - r) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        return max_drawdown
        
        pass