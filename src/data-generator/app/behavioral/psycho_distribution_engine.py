import uuid
import numpy as np
from typing import Dict, Any


class PsychoBehavioralDistributionEngine:
    """
    Математический генератор биомаркеров трат, ночной тревожности
    и психоэмоционального истощения, согласованный с жизненной драмой от LLM.
    """

    @staticmethod
    def synthesize_psycho_features(persona: Dict[str, Any]) -> Dict[str, Any]:
        crisis = persona["life_crisis_type"]
        income = float(persona["declared_income"])

        # Базовые распределения для стабильного гармоничного заемщика (STABLE_HARMONY)
        pharmacy_antidepressant_share = float(np.random.beta(1, 25))        # < 3% чеков в аптеках
        clinical_therapy_spend = 0.0
        nighttime_alcohol_spend = float(np.random.beta(1, 15))              # мало трат на алкоголь
        gambling_outflow = 0.0
        self_care_drop_rate = float(np.random.uniform(0.0, 0.15))           # уход за собой в норме

        sleep_disruption_night_orders = int(np.random.poisson(0.3))         # нет ночной бессонницы
        night_dbo_logins = int(np.random.poisson(0.4))                      # редкие ночные входы
        dwell_time_screen = float(np.random.uniform(5.0, 20.0))             # обычный просмотр графика
        balance_check_frequency = float(np.random.uniform(1.0, 2.5))        # 1-2 раза в день
        support_chat_desperation = 0.0                                      # спокойный тон

        alimony_burden = float(persona.get("alimony_share", 0.0))
        p2p_borrowing_count = int(np.random.poisson(0.2))
        utility_debt_months = 0

        salary_trend_post_crisis = float(np.random.normal(1.02, 0.04))      # стабильная зарплата
        dti_estimate = float(np.random.uniform(0.22, 0.40))

        target_depression_crisis = 0
        target_default_30d = 0
        recommended_empathic_action = "STANDARD_MONITORING"

        # Моделирование специфических психотравм и реакций организма
        if crisis == "DIVORCE_DEPRESSION":
            # Мужчина/женщина после развода: раздел, алименты, депрессивный ступор
            alimony_burden = float(np.random.choice([0.25, 0.33, 0.50]))
            self_care_drop_rate = float(np.random.uniform(0.60, 0.95))      # перестает следить за собой
            pharmacy_antidepressant_share = float(np.random.uniform(0.12, 0.35)) # успокоительные
            clinical_therapy_spend = float(np.random.choice([0.0, 25000.0, 60000.0]))
            nighttime_alcohol_spend = float(np.random.uniform(0.10, 0.30))  # попытка заглушить боль
            sleep_disruption_night_orders = int(np.random.randint(4, 12))   # бессонница
            night_dbo_logins = int(np.random.randint(5, 16))                # ночные приступы тревоги
            dwell_time_screen = float(np.random.uniform(65.0, 160.0))       # ступор на экране кредита
            balance_check_frequency = float(np.random.uniform(5.0, 12.0))
            salary_trend_post_crisis = float(np.random.uniform(0.55, 0.80)) # падение доходов на работе
            dti_estimate = float(np.random.uniform(0.58, 0.88))
            utility_debt_months = int(np.random.choice([0, 1, 2]))
            target_depression_crisis = 1
            target_default_30d = 1
            recommended_empathic_action = "CARE_DIVORCE_HOLIDAYS_3M"

        elif crisis == "BEREAVEMENT_GRIEF":
            # Смерть близкого человека: скорбь, ритуальные траты, оцепенение
            pharmacy_antidepressant_share = float(np.random.uniform(0.20, 0.45))
            self_care_drop_rate = float(np.random.uniform(0.70, 1.0))
            sleep_disruption_night_orders = int(np.random.randint(6, 18))
            night_dbo_logins = int(np.random.randint(4, 14))
            dwell_time_screen = float(np.random.uniform(80.0, 200.0))
            p2p_borrowing_count = int(np.random.randint(2, 6))             # займы у родных на похороны
            salary_trend_post_crisis = float(np.random.uniform(0.60, 0.85))
            dti_estimate = float(np.random.uniform(0.55, 0.80))
            target_depression_crisis = 1
            target_default_30d = 1 if np.random.rand() > 0.25 else 0
            recommended_empathic_action = "BEREAVEMENT_DEBT_FREEZE"

        elif crisis == "EMOTIONAL_BURNOUT":
            # Профессиональное выгорание и астения
            self_care_drop_rate = float(np.random.uniform(0.50, 0.80))
            sleep_disruption_night_orders = int(np.random.randint(5, 14))
            night_dbo_logins = int(np.random.randint(6, 18))
            dwell_time_screen = float(np.random.uniform(50.0, 120.0))
            balance_check_frequency = float(np.random.uniform(6.0, 15.0))
            salary_trend_post_crisis = float(np.random.uniform(0.50, 0.72)) # срез бонусов и премий
            dti_estimate = float(np.random.uniform(0.55, 0.85))
            target_depression_crisis = 1
            target_default_30d = 1
            recommended_empathic_action = "BURNOUT_TERM_EXTENSION_35"

        elif crisis == "FAMILY_HEALTH_EMERGENCY":
            # Тяжелая болезнь родственника: все деньги на медицину
            pharmacy_antidepressant_share = float(np.random.uniform(0.35, 0.65)) # огромные траты на лекарства
            clinical_therapy_spend = float(np.random.uniform(40000.0, 180000.0))
            p2p_borrowing_count = int(np.random.randint(4, 10))
            dti_estimate = float(np.random.uniform(0.65, 0.95))
            utility_debt_months = int(np.random.choice([1, 2, 3]))
            target_depression_crisis = 1
            target_default_30d = 1
            recommended_empathic_action = "HEALTH_EMERGENCY_DEFERRAL"

        elif crisis == "ADDICTION_ESCAPISM":
            # Азартные игры и ночные алкомаркеты как побег от проблем
            nighttime_alcohol_spend = float(np.random.uniform(0.25, 0.55))
            gambling_outflow = float(income * np.random.uniform(0.25, 0.70))
            night_dbo_logins = int(np.random.randint(8, 25))
            balance_check_frequency = float(np.random.uniform(8.0, 20.0))
            dti_estimate = float(np.random.uniform(0.70, 1.10))
            utility_debt_months = int(np.random.randint(1, 4))
            target_depression_crisis = 1
            target_default_30d = 1
            recommended_empathic_action = "RESTRICTIVE_RESTRUCTURING"

        # Расчет итогового индекса психологического истощения (Depression Index: 0.0 - 1.0)
        depression_index = (
            0.25 * (self_care_drop_rate) +
            0.20 * min(1.0, pharmacy_antidepressant_share * 3.0) +
            0.20 * min(1.0, night_dbo_logins / 15.0) +
            0.20 * min(1.0, (1.0 - min(1.0, salary_trend_post_crisis))) +
            0.15 * min(1.0, dwell_time_screen / 150.0)
        )
        depression_index = round(float(np.clip(depression_index, 0.02, 0.99)), 3)

        return {
            "client_token": str(uuid.uuid4()),
            "full_name": persona["full_name"],
            "iin": persona["iin"],
            "age": persona["age"],
            "gender": persona["gender"],
            "city": persona["city"],
            "employment_type": persona["employment_type"],
            "industry": persona["industry"],
            "declared_income": income,
            "life_crisis_type": crisis,
            "life_narrative": persona["life_narrative"],
            # Психоэмоциональные маркеры
            "depression_risk_index": depression_index,
            "pharmacy_antidepressant_share": round(pharmacy_antidepressant_share, 3),
            "clinical_therapy_spending_30d": round(clinical_therapy_spend, 1),
            "nighttime_alcohol_spend_share": round(nighttime_alcohol_spend, 3),
            "gambling_escapism_outflow": round(gambling_outflow, 1),
            "self_care_drop_rate": round(self_care_drop_rate, 3),
            "sleep_disruption_night_orders": sleep_disruption_night_orders,
            "night_dbo_login_frequency": night_dbo_logins,
            "dwell_time_repayment_screen": round(dwell_time_screen, 1),
            "balance_check_anxiety_index": round(balance_check_frequency, 2),
            "support_chat_desperation_score": round(support_chat_desperation, 2),
            "alimony_burden_ratio": round(alimony_burden, 2),
            "p2p_borrowing_from_friends_count": p2p_borrowing_count,
            "utility_debt_months": utility_debt_months,
            "salary_trend_post_crisis": round(salary_trend_post_crisis, 3),
            "dti_dynamic_estimate": round(dti_estimate, 3),
            # Таргеты
            "target_depression_crisis": target_depression_crisis,
            "target_default_30d": target_default_30d,
            "recommended_empathic_action": recommended_empathic_action,
        }
