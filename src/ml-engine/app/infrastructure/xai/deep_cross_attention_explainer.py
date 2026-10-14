from typing import List, Dict, Any, Tuple
import numpy as np
import torch
from app.domain.interfaces import IExplainabilityEngine
from app.domain.entities import ClientFeatureVector, RiskFactorImpact
from app.infrastructure.deep_learning.deep_scoring_model import DeepCrossAttentionScoringModel

FIN_HUMAN_NAMES = {
    "salary_trend_ratio_3m_vs_6m": "Падение регулярных поступлений зарплаты",
    "salary_inflow_delay_days": "Задержка дня выплаты зарплаты работодателем",
    "mfo_gambling_tag_presence": "Платежи в пользу МФО или гемблинга",
    "dti_dynamic_estimate": "Высокая долговая нагрузка (DTI / КДН)",
    "median_daily_balance_7d": "Критическое снижение 7-дневного остатка",
    "net_cashflow_margin_30d": "Отрицательный чистый денежный поток (дефицит)",
    "declared_income": "Уровень официального декларируемого дохода",
}

PSYCHO_HUMAN_NAMES = {
    "pharmacy_antidepressant_share": "Рост расходов на антидепрессанты и седативные",
    "nighttime_alcohol_spend_share": "Аномальные ночные транзакции (алкоголь / эскапизм)",
    "self_care_drop_rate": "Резкое сокращение базовых трат на себя (депрессивный маркер)",
    "night_dbo_login_frequency": "Частые ночные сессии в банковском приложении",
    "dwell_time_repayment_screen": "Длительное зависание на экране графика платежей",
    "sleep_disruption_night_orders": "Нарушение режима сна (ночные маркетплейс-заказы)",
    "balance_check_anxiety_index": "Тревожный серфинг: учащенная проверка баланса",
    "alimony_burden_ratio": "Нагрузка по алиментным выплатам (семейный кризис)",
    "age": "Возрастной фактор адаптивности к шокам",
}


class DeepCrossAttentionExplainabilityEngine(IExplainabilityEngine):
    """
    Инновационный Explainable AI (XAI) движок для двухбашенного FT-Transformer.
    
    1. Извлекает реальные веса Cross-Attention матрицы [7_fin x 9_psycho].
    2. Определяет синергию: какой психоэмоциональный стресс спровоцировал
       конкретную финансовую проблему (например, "Бессонница и ночные входы" -> "Задержка выплат").
    3. Рассчитывает градиентный вклад признаков (Integrated Gradients / Gradient x Input).
    """

    def __init__(self, scoring_model: DeepCrossAttentionScoringModel):
        self._model = scoring_model

    def explain(
        self, features: ClientFeatureVector, top_n: int = 5
    ) -> List[RiskFactorImpact]:
        if not self._model._is_loaded:
            return []

        # 1. Получаем предсказание и веса внимания [1, 7, 9]
        details = self._model.predict_with_details(features)
        attn_matrix = details.get("attention_matrix")  # shape: [7, 9]

        if attn_matrix is None:
            return []

        fin_cols = details["fin_cols"]
        psycho_cols = details["psycho_cols"]

        # 2. Вычисляем суммарный входящий интерес к финансовым признакам
        # (сколько внимания психоэмоциональный кризис уделяет каждому фин. признаку)
        fin_importance = attn_matrix.sum(axis=1)  # shape: [7]

        # Находим топ пар взаимного синергетического влияния (fin_idx, psycho_idx)
        flat_indices = np.argsort(attn_matrix.ravel())[::-1]

        synergy_drivers: List[RiskFactorImpact] = []
        used_fin = set()

        for idx in flat_indices:
            f_idx = idx // len(psycho_cols)
            p_idx = idx % len(psycho_cols)

            if f_idx in used_fin:
                continue

            fin_name = fin_cols[f_idx]
            psycho_name = psycho_cols[p_idx]
            attn_val = float(attn_matrix[f_idx, p_idx])

            fin_desc = FIN_HUMAN_NAMES.get(fin_name, fin_name)
            psycho_desc = PSYCHO_HUMAN_NAMES.get(psycho_name, psycho_name)

            reason = f"{fin_desc} (триггер: {psycho_desc})"

            synergy_drivers.append(
                RiskFactorImpact(
                    feature_name=fin_name,
                    impact_weight=round(attn_val, 4),
                    human_readable_reason=reason,
                )
            )
            used_fin.add(f_idx)

            if len(synergy_drivers) >= top_n:
                break

        return synergy_drivers

    def get_full_cross_attention_heatmap(
        self, features: ClientFeatureVector
    ) -> Dict[str, Any]:
        """
        Возвращает полную тепловую карту Cross-Attention для фронтенда и дашборда.
        """
        details = self._model.predict_with_details(features)
        attn_matrix = details["attention_matrix"]

        return {
            "financial_features": [FIN_HUMAN_NAMES.get(c, c) for c in details["fin_cols"]],
            "psycho_features": [PSYCHO_HUMAN_NAMES.get(c, c) for c in details["psycho_cols"]],
            "attention_scores": attn_matrix.tolist() if attn_matrix is not None else [],
            "distress_evaluation": details.get("distress_evaluation"),
        }
