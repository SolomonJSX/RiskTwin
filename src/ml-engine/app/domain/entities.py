from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum


@dataclass(frozen=True)
class ClientFeatureVector:
    """Полный вектор признаков заемщика (согласно банковской специфике КЗ)."""
    client_token: str
    
    # Группа 1: Динамика и устойчивость доходов
    salary_trend_ratio_3m_vs_6m: float
    salary_inflow_delay_days: int
    inflow_source_entropy: float
    net_cashflow_margin_30d: float

    # Группа 2: Маркеры стресса
    atm_cash_out_intensity: float
    credit_to_debit_transfer_ratio: float
    essential_spending_share_trend: float
    balance_zero_out_frequency: int
    mfo_gambling_tag_presence: bool

    # Группа 3: ДБО и телеметрия
    balance_check_frequency_surge: float
    loan_schedule_screen_dwell_time: float
    support_chat_keyword_velocity: float
    microloan_calculator_views: int

    # Группа 4: Долговая нагрузка
    dti_dynamic_estimate: float
    active_bnpl_installment_count: int
    grace_period_exhaustion_rate: float
    early_payment_decay_days: int

    # Группа 5: Скользящие окна
    median_daily_balance_7d: float
    median_daily_balance_30d: float
    median_daily_balance_90d: float
    p2p_outflow_sum_7d: float
    p2p_outflow_sum_30d: float
    failed_autopay_attempts_30d: int

    def to_feature_dict(self) -> Dict[str, float]:
        """Преобразование вектора в словарь числовых фичей для моделей."""
        return {
            "salary_trend_ratio_3m_vs_6m": self.salary_trend_ratio_3m_vs_6m,
            "salary_inflow_delay_days": float(self.salary_inflow_delay_days),
            "inflow_source_entropy": self.inflow_source_entropy,
            "net_cashflow_margin_30d": self.net_cashflow_margin_30d,
            "atm_cash_out_intensity": self.atm_cash_out_intensity,
            "credit_to_debit_transfer_ratio": self.credit_to_debit_transfer_ratio,
            "essential_spending_share_trend": self.essential_spending_share_trend,
            "balance_zero_out_frequency": float(self.balance_zero_out_frequency),
            "mfo_gambling_tag_presence": 1.0 if self.mfo_gambling_tag_presence else 0.0,
            "balance_check_frequency_surge": self.balance_check_frequency_surge,
            "loan_schedule_screen_dwell_time": self.loan_schedule_screen_dwell_time,
            "support_chat_keyword_velocity": self.support_chat_keyword_velocity,
            "microloan_calculator_views": float(self.microloan_calculator_views),
            "dti_dynamic_estimate": self.dti_dynamic_estimate,
            "active_bnpl_installment_count": float(self.active_bnpl_installment_count),
            "grace_period_exhaustion_rate": self.grace_period_exhaustion_rate,
            "early_payment_decay_days": float(self.early_payment_decay_days),
            "median_daily_balance_7d": self.median_daily_balance_7d,
            "median_daily_balance_30d": self.median_daily_balance_30d,
            "median_daily_balance_90d": self.median_daily_balance_90d,
            "p2p_outflow_sum_7d": self.p2p_outflow_sum_7d,
            "p2p_outflow_sum_30d": self.p2p_outflow_sum_30d,
            "failed_autopay_attempts_30d": float(self.failed_autopay_attempts_30d),
        }


@dataclass(frozen=True)
class RiskFactorImpact:
    feature_name: str
    impact_weight: float  # SHAP value (+ повышает риск, - снижает)
    human_readable_reason: str = ""


@dataclass(frozen=True)
class ScoringPrediction:
    client_token: str
    p_default_30d: float
    p_default_60d: float
    is_high_risk: bool
    top_risk_drivers: List[RiskFactorImpact] = field(default_factory=list)


class ScenarioType(Enum):
    UNSPECIFIED = 0
    PAYMENT_HOLIDAY = 1
    TERM_EXTENSION = 2
    GRACE_PERIOD = 3


@dataclass(frozen=True)
class LoanRestructureScenario:
    scenario_type: ScenarioType
    title: str
    description: str
    new_term_months: int
    new_monthly_payment: float
    grace_period_months: int
    npv_recovery_rate: float
    complies_with_arrfr: bool
    default_probability_under_plan: float = 0.0