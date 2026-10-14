import pickle
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd
from app.domain.interfaces import IExplainabilityEngine
from app.domain.entities import ClientFeatureVector, RiskFactorImpact


# Человекочитаемые описания факторов для кабинета риск-офицера и АРРФР
FEATURE_HUMAN_REASONS = {
    "mfo_gambling_tag_presence": "Платежи в адрес микрофинансовых организаций (МФО) и гемблинга за 30 дней",
    "salary_trend_ratio_3m_vs_6m": "Критическое падение регулярного зарплатного потока (> 25%)",
    "dti_dynamic_estimate": "Превышение регуляторного коэффициента долговой нагрузки КДН (DTI > 50%)",
    "failed_autopay_attempts_30d": "Сбои регулярных автосписаний из-за нехватки остатка на счете",
    "active_bnpl_installment_count": "Избыточное накопление параллельных рассрочек BNPL (0-0-12 / 0-0-24)",
    "balance_zero_out_frequency": "Частое обнуление остатка на счетах (менее 1000 KZT в течение месяца)",
    "microloan_calculator_views": "Аномальный интерес к микрозаймам в приложении банка без фактического оформления",
    "balance_check_frequency_surge": "Всплеск тревожности: учащение проверок баланса в ДБО в 3+ раза к норме",
    "salary_inflow_delay_days": "Задержка исторического дня выплаты зарплаты работодателем",
    "net_cashflow_margin_30d": "Отрицательный чистый денежный поток (проедание подушки безопасности)",
    "credit_to_debit_transfer_ratio": "Переводы с кредитных карт/овердрафтов для закрытия бытовых трат",
    "essential_spending_share_trend": "Режим жесткой экономии: рост доли базовых трат (еда/аптеки) до 90%+",
}


class ShapExplainabilityEngine(IExplainabilityEngine):
    """
    Модуль интерпретируемости XAI на базе реального shap.TreeExplainer.
    Вычисляет точный вклад Шепли каждого признака в итоговый риск-скор.
    """

    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        explainer_path = base_dir / "models" / "archive" / "shap_explainer.pkl"
        if not explainer_path.exists():
            explainer_path = base_dir / "models" / "shap_explainer.pkl"
        cols_path = base_dir / "models" / "archive" / "feature_columns.pkl"
        if not cols_path.exists():
            cols_path = base_dir / "models" / "feature_columns.pkl"

        if explainer_path.exists() and cols_path.exists():
            with open(explainer_path, "rb") as f:
                self.explainer = pickle.load(f)
            with open(cols_path, "rb") as f:
                self.feature_cols = pickle.load(f)
            self._is_loaded = True
        else:
            self._is_loaded = False

    def explain(
        self, features: ClientFeatureVector, top_n: int = 5
    ) -> List[RiskFactorImpact]:
        if not self._is_loaded:
            return []

        f_dict = features.to_feature_dict()
        df_row = pd.DataFrame([f_dict])[self.feature_cols]

        # 1. Расчет реальных значений TreeSHAP для класса 1 (преддефолт)
        shap_vals = self.explainer.shap_values(df_row)

        # Обработка формата возврата shap_values (в зависимости от версии shap)
        if isinstance(shap_vals, list):
            instance_shap = shap_vals[1][0]  # Класс 1
        elif len(shap_vals.shape) == 3:
            instance_shap = shap_vals[0, :, 1]
        else:
            instance_shap = shap_vals[0]

        # 2. Формирование списка факторов
        impacts: List[RiskFactorImpact] = []
        for feat_name, val in zip(self.feature_cols, instance_shap):
            if abs(val) > 0.001:  # Значимые факторы
                reason = FEATURE_HUMAN_REASONS.get(
                    feat_name, f"Фактор финансового поведения: {feat_name}"
                )
                impacts.append(
                    RiskFactorImpact(
                        feature_name=feat_name,
                        impact_weight=round(float(val), 4),
                        human_readable_reason=reason,
                    )
                )

        # 3. Сортировка по силе влияния на повышение риска
        impacts.sort(key=lambda x: x.impact_weight, reverse=True)
        return impacts[:top_n]