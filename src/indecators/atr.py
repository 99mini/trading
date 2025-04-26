import pandas as pd
import numpy as np

def get_atr(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Average True Range(ATR) 계산

    Parameters:
    df (pd.DataFrame): OHLCV 데이터프레임
    period (int): ATR 계산 기간

    Returns:
    pd.Series: ATR 값
    """
    # True Range 계산
    df = df.copy()
    df['prev_close'] = df['close'].shift(1)
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['prev_close'])
    df['tr3'] = abs(df['low'] - df['prev_close'])
    df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)

    # Exponential Moving Average로 ATR 계산 (터틀 트레이딩 방식)
    # ATR = (19 * 이전 ATR + 현재 TR) / 20
    atr_series = pd.Series(index=df.index)
    atr_series.iloc[period] = df['tr'].iloc[1:period+1].mean() # 초기 ATR은 단순 평균으로 계산

    for i in range(period+1, len(df)):
        atr_series.iloc[i] = (19 * atr_series.iloc[i-1] + df['tr'].iloc[i]) / 20

    return atr_series

def get_position_size_for_atr(capital: float, atr: float, volatility_target: float = 0.25) -> float:
    """
    변동성 타겟팅 기반 포지션 사이즈 계산

    Parameters:
    capital (float): 투자 가능 자본
    atr (float): ATR 값
    volatility_target (float): 목표 변동성 (연간 기준)

    Returns:
    float: 투자 단위 크기
    """
    # 터틀 트레이딩 원칙: unit = 자본의 1% / ATR
    # 논문 방식: 변동성 타겟팅 (연간 변동성 25% 목표)
    daily_volatility_target = volatility_target / np.sqrt(252)

    # ATR을 일일 변동성의 프록시로 사용
    risk_per_unit = atr

    # 목표 변동성을 달성하기 위한 포지션 크기 계산
    position_size = (capital * daily_volatility_target) / risk_per_unit

    return position_size