import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any

class AgentArchetype(str, Enum):
    CONSERVATIVE = "CONSERVATIVE"      # Бережливый, стабильный поток, риск 3-8%
    TECH_OPTIMIST = "TECH_OPTIMIST"    # Высокий доход, умеренный риск 10-20%
    IMPULSIVE = "IMPULSIVE"            # Шопоголик, риск легко взлетает до 40-70%
    VULNERABLE = "VULNERABLE"          # Низкий доход, риск балансирует около 60-85%
    PRAGMATIC = "PRAGMATIC"            # Рациональный плательщик, риск 8-15%

class ActionType(str, Enum):
    FREELANCE_INCOME = "FREELANCE_INCOME"              # Дополнительный заработок / бонус
    FAMILY_SUPPORT = "FAMILY_SUPPORT"                  # Помощь/поддержка от близких
    INSTALLMENT_PAID = "INSTALLMENT_PAID"              # Своевременная выплата рассрочки
    EXPENSE_OPTIMIZED = "EXPENSE_OPTIMIZED"            # Сокращение дискреционных трат / покупки
    SALARY_ON_TIME = "SALARY_ON_TIME"                  # Регулярная зарплата вовремя
    SALARY_DELAY = "SALARY_DELAY"                      # Задержка зарплаты работодателем
    NIGHT_APP_CHECK = "NIGHT_APP_CHECK"                # Ночная проверка лимитов в ДБО
    FAILED_AUTOPAY = "FAILED_AUTOPAY"                  # Сбой автоплатежа из-за нехватки средств
    IMPULSE_PURCHASE = "IMPULSE_PURCHASE"              # Спонтанные крупные расходы
    MICROLOAN_TAKEN = "MICROLOAN_TAKEN"                # Срочный займ в МФО

@dataclass
class AgentState:
    agent_id: str
    name: str
    archetype: AgentArchetype
    monthly_income: float
    wallet_balance: float
    monthly_payment: float
    total_debt: float
    account_number: str
    client_token: str
    role: str = ""
    avatar: str = "👤"
    probability_of_default: float = 0.0105  # PD: 0.0 - 1.0
    days_to_payment: int = 18
    is_alive: bool = True
    history: List[Dict[str, Any]] = field(default_factory=list)

    # Динамические 360° признаки из датасета
    ext_source_2: float = 0.88
    salary_trend: float = 1.0
    salary_delay: float = 0.0
    inst_avg_delay_days: float = -5.4
    inst_late_count: float = 0.0
    inst_underpay_count: float = 0.0
    pos_completed_count: float = 2.0
    pos_spend: float = 320000.0
    atm_cash: float = 0.0
    card_utilization: float = 0.18
    external_debt: float = 0.0
    refused_cnt: float = 0.0
    dbo_night_checks: int = 0
    simulation_step: int = 0
    installments_paid_total: int = 36

    # Объективные метрики психологического и поведенческого дистресса (Unsupervised GMM)
    distress_score: float = 0.05
    distress_cluster_code: str = "STABLE_DISCIPLINE"
    distress_cluster_name: str = "Финансовая устойчивость и самоконтроль"
    distress_risk_level: str = "LOW"
    distress_drivers: List[Dict[str, Any]] = field(default_factory=list)
    distress_features: Dict[str, float] = field(default_factory=dict)

    def apply_risk_delta(self, delta_pd: float):
        """Плавное изменение вероятности дефолта с ограничением в диапазоне [0.005, 0.98]"""
        self.probability_of_default = round(max(0.005, min(0.98, self.probability_of_default + delta_pd)), 4)

    def to_dict(self) -> Dict[str, Any]:
        dti = round((self.monthly_payment / max(1.0, self.monthly_income * self.salary_trend)) * 100, 1)
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "avatar": self.avatar,
            "archetype": self.archetype.value,
            "monthly_income": round(self.monthly_income * self.salary_trend, 2),
            "wallet_balance": round(self.wallet_balance, 2),
            "monthly_payment": round(self.monthly_payment, 2),
            "total_debt": round(self.total_debt, 2),
            "account_number": self.account_number,
            "client_token": self.client_token,
            "probability_of_default": round(self.probability_of_default * 100, 2), # в процентах %
            "days_to_payment": self.days_to_payment,
            "dti_ratio": dti,
            "ext_source_2": self.ext_source_2,
            "inst_avg_delay_days": round(self.inst_avg_delay_days, 2),
            "pos_completed_count": int(self.pos_completed_count),
            "card_utilization": round(self.card_utilization * 100, 1),
            "pos_spend": round(self.pos_spend, 2),
            "atm_cash": round(self.atm_cash, 2),
            "simulation_step": self.simulation_step,
            "history_count": len(self.history),
            "distress_score": round(self.distress_score, 4),
            "distress_cluster_code": self.distress_cluster_code,
            "distress_cluster_name": self.distress_cluster_name,
            "distress_risk_level": self.distress_risk_level,
            "distress_drivers": self.distress_drivers,
            "distress_features": self.distress_features,
        }
