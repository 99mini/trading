from .base_strategy import BaseStrategy
import pandas as pd

class VolatilityBreakoutStrategy(BaseStrategy):
    def __init__(self, k=0.5, min_data_points=10):
        self.k = k
        self.min_data_points = min_data_points  # 최소 데이터 요구량 설정

    def generate_signal(self, data):
        if len(data) < self.min_data_points:
            return "hold"
        
        # 마지막 2일 데이터 추출
        latest_data = data.iloc[-2:]
        prev_day = latest_data.iloc[0]
        today = latest_data.iloc[1]
        
        range_ = prev_day['high'] - prev_day['low']
        target = today['open'] + range_ * self.k

        if today['high'] >= target:
            # 목표가 도달 시 매수
            return "buy"
        elif today['low'] <= target:
            # 목표가 하회 시 매도
            return "sell"
        # 목표가 도달하지 않은 경우 보유
        # 또는 매도 신호 없음
        return "hold"
    
    def prepare_data(self, raw_data):
        df = raw_data.copy()
        
        # 필수 컬럼 검증
        required_cols = ['open', 'high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Missing required price columns")
            
        # 데이터 전처리
        df['range'] = df['high'] - df['low']
        df['target'] = df['open'] + df['range'].shift(1) * self.k
        
        # 첫 1일 제거 대신 유효 데이터 시작점 표시
        return df[df['target'].notna()].reset_index(drop=True)
    
    def __name__(self):
        return "VolatilityBreakoutStrategy"
