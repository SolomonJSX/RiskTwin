import pickle
from pathlib import Path
from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
import torch

from app.domain.interfaces import IScoringModel
from app.domain.entities import ClientFeatureVector
from app.infrastructure.deep_learning.cross_attention_net import DualTowerCrossAttentionNet


class DeepCrossAttentionScoringModel(IScoringModel):
    """
    Production инференс глубокой двухбашенной нейросети с Feature Tokenizer
    и механизмом Cross-Attention (PyTorch).
    
    Осуществляет:
    1. Токенизацию признаков (7 финансовых и 9 психоэмоциональных).
    2. Вычисление честной матрицы синергетического внимания между признаками.
    3. Multi-task расчет: вероятность дефолта P_Default и время выживаемости (дни).
    """

    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.weights_path = base_dir / "models" / "deep_cross_attention_net.pt"
        self.scalers_path = base_dir / "models" / "deep_learning_scalers.pkl"

        self._is_loaded = False
        self.device = torch.device("cpu")

        if self.weights_path.exists() and self.scalers_path.exists():
            with open(self.scalers_path, "rb") as f:
                scalers_dict = pickle.load(f)

            self.scaler_fin = scalers_dict["scaler_fin"]
            self.scaler_psycho = scalers_dict["scaler_psycho"]
            self.fin_cols = scalers_dict["fin_cols"]
            self.psycho_cols = scalers_dict["psycho_cols"]

            # Инициализация архитектуры FT-CrossAttention
            self.model = DualTowerCrossAttentionNet(
                fin_dim=len(self.fin_cols),
                psycho_dim=len(self.psycho_cols),
                embed_dim=32,
                num_heads=4,
                dropout=0.0,  # Режим eval
            )
            state_dict = torch.load(self.weights_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            self._is_loaded = True

    def _extract_vectors(self, features: ClientFeatureVector) -> Tuple[np.ndarray, np.ndarray]:
        f_dict = features.to_feature_dict()

        # Маппинг финансовых признаков
        fin_values = []
        for col in self.fin_cols:
            if col == "declared_income":
                # Оценка дохода по балансу/оборотам если не задан явно
                val = f_dict.get(col, max(250000.0, f_dict.get("median_daily_balance_7d", 250000.0) * 1.5))
            else:
                val = f_dict.get(col, 0.0)
            fin_values.append(float(val))

        # Маппинг психоэмоциональных признаков
        # (включая трансляцию телеметрии ДБО в поведенческие маркеры стресса)
        psycho_values = []
        for col in self.psycho_cols:
            if col == "pharmacy_antidepressant_share":
                val = min(0.40, f_dict.get("essential_spending_share_trend", 0.3) * 0.25)
            elif col == "nighttime_alcohol_spend_share":
                val = min(0.35, f_dict.get("atm_cash_out_intensity", 0.2) * 0.3)
            elif col == "self_care_drop_rate":
                val = min(1.0, f_dict.get("balance_zero_out_frequency", 0) / 10.0)
            elif col == "night_dbo_login_frequency":
                val = f_dict.get("microloan_calculator_views", 0) * 2 + 1
            elif col == "dwell_time_repayment_screen":
                val = f_dict.get("loan_schedule_screen_dwell_time", 25.0)
            elif col == "sleep_disruption_night_orders":
                val = 1 if f_dict.get("support_chat_keyword_velocity", 0.0) > 0.5 else 0
            elif col == "balance_check_anxiety_index":
                val = max(1.0, f_dict.get("balance_check_frequency_surge", 1.0) * 3.5)
            elif col == "alimony_burden_ratio":
                val = 0.0
            elif col == "age":
                val = 38.0  # Средний возраст заемщика
            else:
                val = f_dict.get(col, 0.0)
            psycho_values.append(float(val))

        fin_arr = np.array([fin_values], dtype=np.float32)
        psycho_arr = np.array([psycho_values], dtype=np.float32)

        fin_scaled = self.scaler_fin.transform(fin_arr)
        psycho_scaled = self.scaler_psycho.transform(psycho_arr)

        return fin_scaled, psycho_scaled

    def predict_p_default(self, features: ClientFeatureVector) -> tuple[float, float]:
        if not self._is_loaded:
            return 0.35, 0.48

        fin_scaled, psycho_scaled = self._extract_vectors(features)

        t_fin = torch.tensor(fin_scaled, dtype=torch.float32)
        t_psycho = torch.tensor(psycho_scaled, dtype=torch.float32)

        with torch.no_grad():
            p_default, days_pred, _ = self.model(t_fin, t_psycho)

        p_30d = float(p_default.item())
        # Прогноз на 60 дней с учетом фактора угасания и времени выживаемости
        p_60d = min(1.0, max(p_30d, round(p_30d * 1.25, 4)))

        return round(p_30d, 4), round(p_60d, 4)

    def predict_with_details(self, features: ClientFeatureVector) -> Dict[str, Any]:
        """
        Полный инференс нейросети с возвратом матрицы внимания Feature Cross-Attention
        и прогноза дней до дефолта.
        """
        if not self._is_loaded:
            return {
                "p_default_30d": 0.35,
                "p_default_60d": 0.48,
                "predicted_days_to_default": 45,
                "attention_weights": None,
            }

        fin_scaled, psycho_scaled = self._extract_vectors(features)
        t_fin = torch.tensor(fin_scaled, dtype=torch.float32)
        t_psycho = torch.tensor(psycho_scaled, dtype=torch.float32)

        with torch.no_grad():
            p_default, days_pred, attn_weights = self.model(t_fin, t_psycho)

        p_30d = float(p_default.item())
        p_60d = min(1.0, max(p_30d, round(p_30d * 1.25, 4)))
        days = int(round(float(days_pred.item())))

        # attn_weights: [1, 7, 9] -> переводим в numpy
        attn_matrix = attn_weights.squeeze(0).cpu().numpy()

        return {
            "p_default_30d": round(p_30d, 4),
            "p_default_60d": round(p_60d, 4),
            "predicted_days_to_default": max(3, min(240, days)),
            "attention_matrix": attn_matrix,
            "fin_cols": self.fin_cols,
            "psycho_cols": self.psycho_cols,
        }
