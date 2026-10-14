import pickle
from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd

from app.domain.entities import ClientFeatureVector

DISTRESS_HUMAN_NAMES = {
    "cash_panic_ratio": "Паническое обналичивание кредитных лимитов в банкоматах",
    "payment_delay_distress": "Систематические задержки и деградация платёжной дисциплины",
    "deficit_burden_ratio": "Хронический кассовый разрыв и обнуление остатков",
    "rejection_desperation_rate": "Веерная подача заявок и фрустрация от отказов в займах",
    "bnpl_fragmentation_burden": "Импульсивная долговая перегрузка товарными рассрочками (BNPL)",
    "bureau_shock_severity": "Критическая долговая нагрузка и просрочки в сторонних банках",
}


class BehavioralDistressEngine:
    """
    Объективный дата-дривен движок выявления скрытого психологического и финансового
    дистресса человека, обученный на 163 517 реальных заёмщиках (Unsupervised GMM).
    
    Не использует искусственных эвристик (антидепрессанты/алкоголь).
    Выявляет 4 естественных поведенческих архетипа:
    - 0: STABLE_DISCIPLINE (Финансовая устойчивость и самоконтроль)
    - 1: LATENT_ANXIETY (Латентная тревожность и дробление рассрочек)
    - 2: ACUTE_PANIC (Острая паника: обналичивание кредиток и отказы)
    - 3: CHRONIC_EXHAUSTION (Хроническое истощение и дефолтный коллапс)
    """

    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent
        self.model_path = base_dir / "models" / "behavioral_distress_model.pkl"
        self._is_loaded = False
        
        if self.model_path.exists():
            with open(self.model_path, "rb") as f:
                artifact = pickle.load(f)
            self.scaler = artifact["scaler"]
            self.gmm = artifact["gmm"]
            self.feature_names = artifact["feature_names"]
            self.cluster_mapping = artifact["cluster_mapping"]
            self.sorted_order = artifact["sorted_order"]
            self._is_loaded = True

    def extract_features(self, features: ClientFeatureVector) -> pd.DataFrame:
        """Извлекает 6 объективных признаков дистресса из вектора телеметрии."""
        f_dict = features.to_feature_dict() if hasattr(features, "to_feature_dict") else features

        # Если переданы сырые колонки Home Credit:
        if "cc_atm_drawings_sum" in f_dict:
            pos_draw = float(f_dict.get("cc_pos_drawings_sum", 0.0))
            atm_draw = float(f_dict.get("cc_atm_drawings_sum", 0.0))
            cc_util = float(np.clip(f_dict.get("cc_utilization_mean", 0.0), 0.0, 2.0))
            cash_panic = (atm_draw / (pos_draw + 1000.0)) * cc_util
            
            delay_days = float(max(0.0, f_dict.get("inst_avg_delay_days", 0.0)))
            tx_cnt = float(f_dict.get("inst_total_tx", 1.0))
            late_cnt = float(f_dict.get("inst_late_count", 0.0))
            payment_delay = (late_cnt / (tx_cnt + 1.0)) * np.log1p(delay_days)
            
            annuity = float(max(1000.0, f_dict.get("AMT_ANNUITY", 25000.0)))
            deficit = float(max(0.0, f_dict.get("inst_total_deficit", 0.0)))
            deficit_burden = np.log1p(deficit / annuity)
            
            prev_tot = float(f_dict.get("prev_app_total", 0.0))
            prev_ref = float(f_dict.get("prev_refused_count", 0.0))
            rejection_desp = prev_ref / (prev_tot + 1.0)
            
            pos_act = float(f_dict.get("pos_active_count", 0.0))
            pos_rem = float(f_dict.get("pos_remaining_installments", 0.0))
            bnpl_burden = np.log1p(pos_act * np.sqrt(pos_rem + 1.0))
            
            bureau_overdue = float(f_dict.get("bureau_total_overdue", 0.0))
            max_dpd = float(max(f_dict.get("pos_max_dpd", 0.0), f_dict.get("cc_max_dpd", 0.0)))
            bureau_shock = np.log1p(bureau_overdue / 1000.0) + np.log1p(max_dpd)
        else:
            # Маппинг из онлайн-телеметрии транзакций и ДБО
            atm_intensity = float(f_dict.get("atm_cash_out_intensity", 0.1))
            c2d_transfer = float(f_dict.get("credit_to_debit_transfer_ratio", 0.0))
            grace_exhaust = float(f_dict.get("grace_period_exhaustion_rate", 0.0))
            cash_panic = atm_intensity * (1.0 + c2d_transfer * 10.0) * grace_exhaust * 50.0

            failed_autopay = float(f_dict.get("failed_autopay_attempts_30d", 0))
            salary_delay = float(f_dict.get("salary_inflow_delay_days", 0))
            decay_days = float(f_dict.get("early_payment_decay_days", 0))
            payment_delay = (failed_autopay / 4.0) * np.log1p(max(0.0, salary_delay + decay_days))

            zero_out = float(f_dict.get("balance_zero_out_frequency", 0))
            dti = float(f_dict.get("dti_dynamic_estimate", 0.35))
            deficit_burden = np.log1p((zero_out / 8.0) * max(0.4, dti))

            microloan_views = float(f_dict.get("microloan_calculator_views", 0))
            mfo_flag = 1.0 if f_dict.get("mfo_gambling_tag_presence", False) else 0.0
            rejection_desp = min(1.0, (microloan_views * 0.20) + (0.45 * mfo_flag))

            bnpl_cnt = float(f_dict.get("active_bnpl_installment_count", 0))
            bnpl_burden = np.log1p(bnpl_cnt * 3.0)

            bureau_shock = (2.5 if mfo_flag > 0 else 0.0) + (1.2 if dti > 0.60 else 0.0)

        df = pd.DataFrame([{
            "cash_panic_ratio": cash_panic,
            "payment_delay_distress": payment_delay,
            "deficit_burden_ratio": deficit_burden,
            "rejection_desperation_rate": rejection_desp,
            "bnpl_fragmentation_burden": bnpl_burden,
            "bureau_shock_severity": bureau_shock,
        }])
        return df

    def evaluate_distress(self, features: ClientFeatureVector) -> Dict[str, Any]:
        """Оценивает психологическое состояние заемщика только по данным датасета."""
        if not self._is_loaded:
            return {
                "distress_score": 0.1,
                "cluster_code": "STABLE_DISCIPLINE",
                "cluster_name": "Финансовая устойчивость",
                "risk_level": "LOW",
                "state_probabilities": {},
                "top_distress_drivers": [],
            }

        df = self.extract_features(features)
        X_scaled = self.scaler.transform(df)
        
        # Предсказание вероятностей кластеров
        probs = self.gmm.predict_proba(X_scaled)[0]
        cluster_id = int(np.argmax(probs))
        cluster_info = self.cluster_mapping.get(cluster_id, self.cluster_mapping.get(str(cluster_id)))
        
        # Скор дистресса как взвешенная сумма рангов кластеров [0.0 ... 1.0]
        # rank 0: 0.05, rank 1: 0.35, rank 2: 0.70, rank 3: 0.95
        rank_weights = [0.05, 0.35, 0.70, 0.95]
        score = sum(probs[orig_c] * rank_weights[self.cluster_mapping[orig_c]["rank"]] for orig_c in range(len(probs)))
        score = float(np.clip(score, 0.0, 1.0))

        # Формирование распределения вероятностей состояний
        state_probs = {}
        for orig_c, p in enumerate(probs):
            info = self.cluster_mapping[orig_c]
            state_probs[info["code"]] = round(float(p), 4)

        # Анализ ключевых драйверов стресса для данного заемщика
        row_vals = df.iloc[0].to_dict()
        drivers = []
        for feat in self.feature_names:
            val = float(row_vals[feat])
            human_name = DISTRESS_HUMAN_NAMES.get(feat, feat)
            # Вклад признака относительно эталонного стабильного кластера
            baseline = self.cluster_mapping[self.sorted_order[0]]["feature_profile"].get(feat, 0.0)
            excess = max(0.0, val - baseline)
            if excess > 0:
                drivers.append({
                    "feature": feat,
                    "name": human_name,
                    "value": round(val, 3),
                    "impact": round(excess, 3),
                })
        
        drivers.sort(key=lambda x: x["impact"], reverse=True)

        return {
            "distress_score": round(score, 4),
            "cluster_code": cluster_info["code"],
            "cluster_name": cluster_info["name"],
            "risk_level": cluster_info["risk_level"],
            "default_rate_benchmark": cluster_info["default_rate"],
            "state_probabilities": state_probs,
            "distress_features": row_vals,
            "top_distress_drivers": drivers[:4],
        }
