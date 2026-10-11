from abc import ABC, abstractmethod
from typing import List, Dict
from app.domain.entities import (
    ClientFeatureVector,
    ScoringPrediction,
    RiskFactorImpact,
    LoanRestructureScenario,
)


class IScoringModel(ABC):
    """Контракт модели расчета вероятности дефолта."""

    @abstractmethod
    def predict_p_default(self, features: ClientFeatureVector) -> tuple[float, float]:
        """Возвращает (p_default_30d, p_default_60d)."""
        pass


class IExplainabilityEngine(ABC):
    """Контракт движка объяснения факторов риска (XAI/SHAP)."""

    @abstractmethod
    def explain(
        self, features: ClientFeatureVector, top_n: int = 5
    ) -> List[RiskFactorImpact]:
        """Возвращает топ N наиболее значимых факторов риска."""
        pass


class IRestructuringOptimizer(ABC):
    """Контракт оптимизатора сценариев реструктуризации."""

    @abstractmethod
    def optimize(
        self,
        client_token: str,
        remaining_principal: float,
        interest_rate: float,
        remaining_term_months: int,
        current_monthly_payment: float,
        estimated_client_capacity: float,
    ) -> List[LoanRestructureScenario]:
        """Генерирует оптимальные сценарии реструктуризации."""
        pass