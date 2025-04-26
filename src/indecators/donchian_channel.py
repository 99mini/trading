import pandas as pd
from typing import Dict, List

def get_donchian_channel(df: pd.DataFrame, period: int) -> Dict[str, pd.Series]:
    """
    Donchian Channel 계산

    Parameters:
    df (pd.DataFrame): OHLCV 데이터프레임
    period (int): 돈치안 채널 계산 기간

    Returns:
    Dict[str, pd.Series]: 상단, 하단, 중간 밴드 시리즈
    """
    upper_band = df['high'].rolling(window=period).max()
    lower_band = df['low'].rolling(window=period).min()
    middle_band = (upper_band + lower_band) / 2

    return {
        'upper': upper_band,
        'lower': lower_band,
        'middle': middle_band
    }

def generate_ensemble_signals(df: pd.DataFrame, lookback_periods: List[int] = [5, 10, 20, 55, 120]) -> pd.Series:
    """
    여러 기간의 Donchian 채널을 앙상블하여 시그널 생성

    Parameters:
    df (pd.DataFrame): OHLCV 데이터프레임
    lookback_periods (List[int]): 앙상블에 사용할 기간 리스트

    Returns:
    pd.Series: 앙상블 시그널 (-1: 매도, 0: 홀드, 1: 매수)
    """
    signals = pd.DataFrame(index=df.index)

    # 각 기간별 돈치안 채널 계산 및 신호 생성
    for period in lookback_periods:
        dc = get_donchian_channel(df, period)

        # 매수 신호: 종가가 상단 밴드 돌파
        # 매도 신호: 종가가 중간 밴드 아래로 하락
        col_name = f'signal_{period}'
        signals[col_name] = 0

        # 매수 조건: 종가가 N일 최고가를 상향 돌파
        buy_condition = (df['close'] > dc['upper'].shift(1))
        # 매도 조건: 종가가 중간 밴드 아래로 하락
        sell_condition = (df['close'] < dc['middle'])

        signals.loc[buy_condition, col_name] = 1
        signals.loc[sell_condition, col_name] = -1

    # 앙상블 신호 계산: 신호들의 평균
    signals['ensemble'] = signals.mean(axis=1)

    # 앙상블 신호 해석: 0.3 이상이면 매수, -0.3 이하면 매도
    ensemble_signal = pd.Series(0, index=df.index)
    ensemble_signal[signals['ensemble'] >= 0.3] = 1
    ensemble_signal[signals['ensemble'] <= -0.3] = -1

    return ensemble_signal