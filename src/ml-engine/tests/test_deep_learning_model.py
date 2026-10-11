import pickle
from pathlib import Path
import pytest
import numpy as np
import torch

from app.infrastructure.deep_learning.cross_attention_net import DualTowerCrossAttentionNet


@pytest.fixture(scope="module")
def dl_model_bundle():
    """Фикстура загрузки весов PyTorch нейросети и скалеров."""
    base_dir = Path(__file__).resolve().parent.parent
    weights_path = base_dir / "models" / "deep_cross_attention_net.pt"
    scalers_path = base_dir / "models" / "deep_learning_scalers.pkl"

    assert weights_path.exists(), "Файл весов deep_cross_attention_net.pt должен существовать"
    assert scalers_path.exists(), "Файл скалеров deep_learning_scalers.pkl должен существовать"

    with open(scalers_path, "rb") as f:
        scalers = pickle.load(f)

    model = DualTowerCrossAttentionNet(
        fin_dim=len(scalers["fin_cols"]),
        psycho_dim=len(scalers["psycho_cols"]),
        embed_dim=32,
        num_heads=4,
        dropout=0.0,
    )
    model.load_state_dict(torch.load(weights_path, map_location="cpu"))
    model.eval()

    return {
        "model": model,
        "scaler_fin": scalers["scaler_fin"],
        "scaler_psycho": scalers["scaler_psycho"],
        "fin_cols": scalers["fin_cols"],
        "psycho_cols": scalers["psycho_cols"],
    }


def prepare_tensors(bundle, fin_dict: dict, psycho_dict: dict):
    """Хелпер нормализации и перевода в PyTorch тензоры."""
    fin_vals = np.array([[fin_dict[col] for col in bundle["fin_cols"]]])
    psycho_vals = np.array([[psycho_dict[col] for col in bundle["psycho_cols"]]])

    fin_scaled = bundle["scaler_fin"].transform(fin_vals)
    psycho_scaled = bundle["scaler_psycho"].transform(psycho_vals)

    fin_tensor = torch.tensor(fin_scaled, dtype=torch.float32)
    psycho_tensor = torch.tensor(psycho_scaled, dtype=torch.float32)

    return fin_tensor, psycho_tensor


# ==============================================================================
# ТЕСТ 1: Проверка размерностей и диапазонов выходов нейросети
# ==============================================================================
def test_network_shapes_and_probability_bounds(dl_model_bundle):
    bundle = dl_model_bundle
    fin_sample = {
        "salary_trend_ratio_3m_vs_6m": 1.0,
        "salary_inflow_delay_days": 0,
        "mfo_gambling_tag_presence": 0,
        "dti_dynamic_estimate": 0.30,
        "median_daily_balance_7d": 150000.0,
        "net_cashflow_margin_30d": 0.20,
        "declared_income": 500000.0,
    }
    psycho_sample = {
        "pharmacy_antidepressant_share": 0.02,
        "nighttime_alcohol_spend_share": 0.02,
        "self_care_drop_rate": 0.05,
        "night_dbo_login_frequency": 0,
        "dwell_time_repayment_screen": 15.0,
        "sleep_disruption_night_orders": 0,
        "balance_check_anxiety_index": 1.2,
        "alimony_burden_ratio": 0.0,
        "age": 35,
    }

    f_t, p_t = prepare_tensors(bundle, fin_sample, psycho_sample)

    with torch.no_grad():
        p_def, days, attn_weights = bundle["model"](f_t, p_t)

    p_val = float(p_def.item())
    days_val = float(days.item())

    assert 0.0 <= p_val <= 1.0, f"Вероятность дефолта обязана лежать в [0, 1], получено: {p_val}"
    assert days_val > 0.0, f"Количество дней до дефолта должно быть положительным, получено: {days_val}"
    # Feature Tokenizer Cross-Attention формирует честную матрицу связей: [Batch, 7_fin_tokens, 9_psycho_tokens]
    assert attn_weights.shape == (1, 7, 9), f"Размерность матрицы кросс-внимания: {attn_weights.shape}"


# ==============================================================================
# ТЕСТ 2: Контраст профилей — Развод и депрессия обязаны увеличивать риск
# ==============================================================================
def test_contrastive_risk_increase_on_divorce_and_distress(dl_model_bundle):
    bundle = dl_model_bundle

    # Профиль А: Здоровый стабильный заемщик
    fin_healthy = {
        "salary_trend_ratio_3m_vs_6m": 1.05,
        "salary_inflow_delay_days": 0,
        "mfo_gambling_tag_presence": 0,
        "dti_dynamic_estimate": 0.25,
        "median_daily_balance_7d": 250000.0,
        "net_cashflow_margin_30d": 0.30,
        "declared_income": 650000.0,
    }
    psycho_healthy = {
        "pharmacy_antidepressant_share": 0.01,
        "nighttime_alcohol_spend_share": 0.01,
        "self_care_drop_rate": 0.05,
        "night_dbo_login_frequency": 0,
        "dwell_time_repayment_screen": 10.0,
        "sleep_disruption_night_orders": 0,
        "balance_check_anxiety_index": 1.0,
        "alimony_burden_ratio": 0.0,
        "age": 38,
    }

    # Профиль Б: Развод, алименты, бессонница, ночные входы в ДБО, спад зарплаты
    fin_stressed = {
        "salary_trend_ratio_3m_vs_6m": 0.65,
        "salary_inflow_delay_days": 14,
        "mfo_gambling_tag_presence": 1,
        "dti_dynamic_estimate": 0.75,
        "median_daily_balance_7d": 15000.0,
        "net_cashflow_margin_30d": -0.25,
        "declared_income": 400000.0,
    }
    psycho_stressed = {
        "pharmacy_antidepressant_share": 0.35,
        "nighttime_alcohol_spend_share": 0.25,
        "self_care_drop_rate": 0.90,
        "night_dbo_login_frequency": 14,
        "dwell_time_repayment_screen": 130.0,
        "sleep_disruption_night_orders": 8,
        "balance_check_anxiety_index": 12.0,
        "alimony_burden_ratio": 0.33,
        "age": 38,
    }

    f_h, p_h = prepare_tensors(bundle, fin_healthy, psycho_healthy)
    f_s, p_s = prepare_tensors(bundle, fin_stressed, psycho_stressed)

    with torch.no_grad():
        p_healthy, days_healthy, _ = bundle["model"](f_h, p_h)
        p_stressed, days_stressed, _ = bundle["model"](f_s, p_s)

    p_h_val = float(p_healthy.item())
    p_s_val = float(p_stressed.item())

    assert p_h_val < 0.40, f"У здорового заемщика скор должен быть умеренным, получено: {p_h_val:.4f}"
    assert p_s_val > 0.60, f"У заемщика в кризисе скор должен быть высоким, получено: {p_s_val:.4f}"
    assert p_s_val > p_h_val + 0.30, f"Дельта риска при кризисе должна быть > 30 п.п., получено: {p_s_val - p_h_val:.4f}"


# ==============================================================================
# ТЕСТ 3: Независимость инференса в батчах (Batch Invariance)
# ==============================================================================
def test_batch_invariance_no_information_leakage(dl_model_bundle):
    bundle = dl_model_bundle

    # Создаем случайный батч из 8 заемщиков
    np.random.seed(42)
    fin_dummy = np.random.randn(8, len(bundle["fin_cols"]))
    psycho_dummy = np.random.randn(8, len(bundle["psycho_cols"]))

    f_b = torch.tensor(fin_dummy, dtype=torch.float32)
    p_b = torch.tensor(psycho_dummy, dtype=torch.float32)

    with torch.no_grad():
        p_batch, _, _ = bundle["model"](f_b, p_b)

        # Проверяем 3-го заемщика отдельно
        p_single, _, _ = bundle["model"](f_b[3:4], p_b[3:4])

    assert np.isclose(float(p_batch[3].item()), float(p_single.item()), atol=1e-5), (
        "Инференс в батче не должен отличаться от одиночного (отсутствие утечек в слоях)"
    )


# ==============================================================================
# ТЕСТ 4: Устойчивость к экстремальным выбросам (No NaN / Overflow)
# ==============================================================================
@pytest.mark.parametrize("extreme_dti,extreme_alimony,extreme_age", [
    (0.0, 0.0, 18),
    (2.5, 0.50, 75),
    (1.2, 0.33, 40),
])
def test_no_nan_on_edge_cases(dl_model_bundle, extreme_dti, extreme_alimony, extreme_age):
    bundle = dl_model_bundle

    fin_edge = {
        "salary_trend_ratio_3m_vs_6m": 0.1,
        "salary_inflow_delay_days": 30,
        "mfo_gambling_tag_presence": 1,
        "dti_dynamic_estimate": extreme_dti,
        "median_daily_balance_7d": 0.0,
        "net_cashflow_margin_30d": -0.8,
        "declared_income": 80000.0,
    }
    psycho_edge = {
        "pharmacy_antidepressant_share": 0.50,
        "nighttime_alcohol_spend_share": 0.50,
        "self_care_drop_rate": 1.0,
        "night_dbo_login_frequency": 30,
        "dwell_time_repayment_screen": 300.0,
        "sleep_disruption_night_orders": 20,
        "balance_check_anxiety_index": 30.0,
        "alimony_burden_ratio": extreme_alimony,
        "age": extreme_age,
    }

    f_t, p_t = prepare_tensors(bundle, fin_edge, psycho_edge)

    with torch.no_grad():
        p_def, days, _ = bundle["model"](f_t, p_t)

    assert not torch.isnan(p_def).any(), "Вероятность не должна содержать NaN"
    assert not torch.isnan(days).any(), "Дни не должны содержать NaN"
    assert not torch.isinf(p_def).any(), "Вероятность не должна уходить в Inf"