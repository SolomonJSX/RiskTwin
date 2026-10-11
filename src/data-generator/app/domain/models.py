from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import uuid


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class EmploymentType(str, Enum):
    OFFICIAL_EMPLOYED = "OFFICIAL_EMPLOYED"       # Официальный найм
    INDIVIDUAL_ENTREPRENEUR = "INDIVIDUAL_ENTREPRENEUR" # ИП
    SELF_EMPLOYED = "SELF_EMPLOYED"               # Самозанятый
    STUDENT = "STUDENT"


class RiskArchetype(str, Enum):
    STABLE = "STABLE"                             # Платежеспособный, без просрочек
    INCOME_SHOCK = "INCOME_SHOCK"                 # Потеря работы / падение зарплаты
    BNPL_OVERLEVERAGED = "BNPL_OVERLEVERAGED"     # Перегруз рассрочками (Kaspi/Halyk 0-0-12/24)
    MFO_DEBT_SPIRAL = "MFO_DEBT_SPIRAL"           # Долговая спираль микрозаймов
    LIQUIDITY_GAP = "LIQUIDITY_GAP"               # Сезонный кассовый разрыв (ИП / самозанятый)


class PersonaProfile(BaseModel):
    """Демографический портрет заемщика, генерируемый LLM."""
    client_token: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    iin: str
    age: int
    gender: Gender
    city: str
    employment_type: EmploymentType
    industry: str
    declared_income: float
    archetype: RiskArchetype
    stress_narrative: str                         # Текстовое описание жизненной ситуации заемщика


class BehavioralFeatures(BaseModel):
    """24 финансовых признака, согласованных с Protobuf-контрактом RiskTwin."""
    # Группа 1: Динамика доходов
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


class SyntheticBorrowerRecord(BaseModel):
    """Полная запись для датасета и банковской базы."""
    persona: PersonaProfile
    features: BehavioralFeatures
    target_default_30d: int                       # 1 - преддефолт, 0 - норма
    predicted_days_to_default: int                # Для Survival Analysis