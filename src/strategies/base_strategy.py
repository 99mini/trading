from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        전략 매매 신호 생성 메인 메서드

        Args:
            data (pd.DataFrame): 전처리 완료된 시계열 데이터
                - 필수 컬럼: `open`, `high`, `low`, `close`
                - 인덱스: datetime 형식 권장

        Returns:
            str: 실행할 거래 신호
                - 가능한 값: `buy` | `sell` | `hold`
        """
        pass
    
    @abstractmethod
    def prepare_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        원시 데이터를 전략에 맞게 전처리

        Args:
            raw_data (pd.DataFrame): 거래소에서 수집한 원시 데이터
                - 기본 컬럼: `timestamp`, `open`, `high`, `low`, `close`, `volume`

        Returns:
            pd.DataFrame: 전략 분석용으로 가공된 데이터프레임
                - 추가 컬럼: 전략별 계산 지표 (예: 이동평균, 변동성 등)
        """
        pass

    @abstractmethod
    def __name__(self) -> str:
        """
        전략 식별용 이름 반환

        Returns:
            str: 전략 클래스 이름 (예: 'VolatilityBreakoutStrategy')
        """
        return self.__class__.__name__
