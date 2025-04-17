import pandas as pd
import os

from strategies import MovingAverageStrategy, VolatilityBreakoutStrategy
from backtesting import Backtester

coins = ['BTCUSDT', 'ETHUSDT']
interval = '5m'
target_data = f'{coins[0]}_{interval}'

def main():
    # 1. 과거 데이터 로드

    data_path = os.path.join(
        os.path.dirname(__file__),
        'assets',
        'data',
        f'{target_data}.csv'
    )

    for strategy in [MovingAverageStrategy, VolatilityBreakoutStrategy]:

        # 2. 백테스팅 설정
        backtester = Backtester(strategy)

        backtester.load_data(data_path)
        
        # 3. 백테스팅 실행
        results = backtester.run()
        
        # 4. 결과 출력
        print("\n🔎 백테스팅 결과 리포트")
        print(f"전략 이름: {strategy.__name__}")
        print(f"투자 코인: {target_data}")
        print(f"테스트 기간: {results['duration'][0]} ~ {results['duration'][-1]}")
        print(f"총 거래 횟수: {results['total_trades']}회")
        print(f"승률: {results['win_rate']:.2f}%")
        print(f"총 수익금: {results['total_return']:.2f}")
        print(f"샤프 지수: {results['sharpe_ratio']:.2f}")
        print(f"최대 손실률: {results['max_drawdown']:.2f}%")

if __name__ == "__main__":
    main()