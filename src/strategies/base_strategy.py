from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> str:
        """
        전략 신호 생성 메서드
        :return: `buy`| `sell` | `hold`
        """
        pass
    
    @abstractmethod
    def prepare_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """백테스팅/트레이딩에 사용할 데이터 전처리"""
        pass

    @abstractmethod
    def __name__(self):
        """전략 이름"""
        return self.__class__.__name__
