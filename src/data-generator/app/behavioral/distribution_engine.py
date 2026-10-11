import numpy as np
from app.domain.models import PersonaProfile, BehavioralFeatures, RiskArchetype


class BehavioralDistributionEngine:
    """
    Генерирует 24 финансовых признака, математически согласованных
    с архетипом риска и жизненной историей от LLM.
    """

    @staticmethod
    def generate_features_for_persona(persona: PersonaProfile) -> tuple[BehavioralFeatures, int, int]:
        income = persona.declared_income
        arch = persona.archetype

        # 1. Базовые распределения для стабильного заемщика (STABLE)
        salary_trend = float(np.random.uniform(0.92, 1.05))
        delay_days = int(np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1]))
        inflow_entropy = float(np.random.normal(1.0, 0.2))
        net_cashflow_margin = float(np.random.uniform(0.10, 0.35))
        atm_intensity = float(np.random.beta(2, 6))
        credit_to_debit = float(np.random.beta(1, 8))
        essential_spending = float(np.random.uniform(0.35, 0.60))
        balance_zero_freq = int(np.random.poisson(1))
        mfo_flag = False
        dbo_surge = float(np.random.uniform(0.8, 1.3))
        loan_dwell_time = float(np.random.uniform(5.0, 25.0))
        support_velocity = float(np.random.poisson(0.2))
        microloan_views = 0
        dti_estimate = float(np.random.uniform(0.25, 0.45))
        bnpl_count = int(np.random.choice([0, 1, 2], p=[0.5, 0.35, 0.15]))
        grace_exhaustion = float(np.random.uniform(0.0, 0.3))
        payment_decay_days = int(np.random.choice([0, 1], p=[0.8, 0.2]))
        failed_autopay = 0

        target_default_30d = 0
        predicted_days_to_default = int(np.random.randint(60, 180))

        # 2. Модификация признаков под конкретный стресс-архетип от LLM
        if arch == RiskArchetype.INCOME_SHOCK:
            salary_trend = float(np.random.uniform(0.45, 0.72))  # Падение зарплаты > 30%
            delay_days = int(np.random.randint(7, 21))          # Задержка выплат
            net_cashflow_margin = float(np.random.uniform(-0.35, -0.05)) # Проедание подушки
            balance_zero_freq = int(np.random.randint(8, 18))
            dbo_surge = float(np.random.uniform(2.5, 5.0))       # Панические проверки баланса
            loan_dwell_time = float(np.random.uniform(60.0, 150.0)) # Изучение графика
            support_velocity = float(np.random.uniform(2.0, 5.0))
            dti_estimate = float(np.random.uniform(0.55, 0.85))  # Резкий рост DTI
            target_default_30d = 1
            predicted_days_to_default = int(np.random.randint(8, 22))

        elif arch == RiskArchetype.BNPL_OVERLEVERAGED:
            bnpl_count = int(np.random.randint(4, 9))            # Множество мелких рассрочек
            grace_exhaustion = float(np.random.uniform(0.75, 1.0))
            credit_to_debit = float(np.random.uniform(0.35, 0.65)) # Погашение рассрочек с кредитки
            essential_spending = float(np.random.uniform(0.75, 0.95))
            dti_estimate = float(np.random.uniform(0.58, 0.78))
            failed_autopay = int(np.random.randint(1, 3))
            target_default_30d = 1
            predicted_days_to_default = int(np.random.randint(14, 28))

        elif arch == RiskArchetype.MFO_DEBT_SPIRAL:
            mfo_flag = True                                      # Критический маркер МФО
            microloan_views = int(np.random.randint(2, 6))
            atm_intensity = float(np.random.uniform(0.5, 0.85))  # Уход в наличные
            inflow_source_entropy = float(np.random.uniform(2.2, 3.8)) # Дробление на случайные P2P
            balance_zero_freq = int(np.random.randint(12, 25))
            dti_estimate = float(np.random.uniform(0.65, 0.95))
            failed_autopay = int(np.random.randint(1, 4))
            target_default_30d = 1
            predicted_days_to_default = int(np.random.randint(5, 15))

        elif arch == RiskArchetype.LIQUIDITY_GAP:
            delay_days = int(np.random.randint(10, 30))          # Кассовый разрыв
            net_cashflow_margin = float(np.random.uniform(-0.25, 0.0))
            loan_dwell_time = float(np.random.uniform(40.0, 90.0))
            dti_estimate = float(np.random.uniform(0.48, 0.65))
            target_default_30d = 1 if np.random.rand() > 0.3 else 0
            predicted_days_to_default = int(np.random.randint(18, 35))

        # 3. Скользящие окна (согласованы с уровнем дохода заемщика)
        median_90d = float(income * np.random.uniform(0.6, 1.4))
        median_30d = float(median_90d * (0.4 if target_default_30d else 0.95))
        median_7d = float(median_30d * (0.2 if target_default_30d else 0.90))

        p2p_sum_7d = float(income * np.random.uniform(0.15, 0.45))
        p2p_sum_30d = float(p2p_sum_7d * np.random.uniform(3.5, 4.8))

        features = BehavioralFeatures(
            salary_trend_ratio_3m_vs_6m=round(salary_trend, 3),
            salary_inflow_delay_days=delay_days,
            inflow_source_entropy=round(inflow_entropy, 2),
            net_cashflow_margin_30d=round(net_cashflow_margin, 3),
            atm_cash_out_intensity=round(atm_intensity, 3),
            credit_to_debit_transfer_ratio=round(credit_to_debit, 3),
            essential_spending_share_trend=round(essential_spending, 3),
            balance_zero_out_frequency=balance_zero_freq,
            mfo_gambling_tag_presence=mfo_flag,
            balance_check_frequency_surge=round(dbo_surge, 2),
            loan_schedule_screen_dwell_time=round(loan_dwell_time, 1),
            support_chat_keyword_velocity=round(support_velocity, 2),
            microloan_calculator_views=microloan_views,
            dti_dynamic_estimate=round(dti_estimate, 3),
            active_bnpl_installment_count=bnpl_count,
            grace_period_exhaustion_rate=round(grace_exhaustion, 3),
            early_payment_decay_days=payment_decay_days,
            median_daily_balance_7d=round(median_7d, 0),
            median_daily_balance_30d=round(median_30d, 0),
            median_daily_balance_90d=round(median_90d, 0),
            p2p_outflow_sum_7d=round(p2p_sum_7d, 0),
            p2p_outflow_sum_30d=round(p2p_sum_30d, 0),
            failed_autopay_attempts_30d=failed_autopay,
        )

        return features, target_default_30d, predicted_days_to_default