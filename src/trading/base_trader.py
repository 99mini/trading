from abc import ABC, abstractmethod
import pandas as pd

class BaseTrader(ABC):
    def __init__(self, strategy):
        self.strategy = strategy
        self.connected = False
    
    @abstractmethod
    def _connect(self):
        """거래소 연결 추상 메서드"""
        pass
    
    @abstractmethod
    def _fetch_data(self, symbol: str, interval: str) -> pd.DataFrame:
        """시장 데이터 조회 추상 메서드"""
        pass
    
    @abstractmethod
    def _execute_order(self, symbol: str, side: str, quantity: float):
        """주문 실행 추상 메서드"""
        pass
    
    def run(self, symbol: str, interval: str):
        if not self.connected:
            self._connect()
            
        data = self._fetch_data(symbol, interval)
        processed_data = self.strategy.prepare_data(data)
        signal = self.strategy.generate_signal(processed_data)
        
        if signal == "buy":
            self._execute_order(symbol, "BUY", 0.001)  # 기본 수량
        elif signal == "sell":
            self._execute_order(symbol, "SELL", 0.001)
