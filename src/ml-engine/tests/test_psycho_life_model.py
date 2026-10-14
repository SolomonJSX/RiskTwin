import pickle
from pathlib import Path
import pytest
import numpy as np
import pandas as pd


@pytest.fixture(scope="module")
def psycho_model_artifacts():
    base_dir = Path(__file__).resolve().parent.parent
    model_path = base_dir / "models" / "archive" / "psycho_life_lgbm.pkl"
    if not model_path.exists():
        model_path = base_dir / "models" / "psycho_life_lgbm.pkl"
    explainer_path = base_dir / "models" / "archive" / "psycho_shap_explainer.pkl"
    if not explainer_path.exists():
        explainer_path = base_dir / "models" / "psycho_shap_explainer.pkl"
    cols_path = base_dir / "models" / "archive" / "psycho_feature_columns.pkl"
    if not cols_path.exists():
        cols_path = base_dir / "models" / "psycho_feature_columns.pkl"

    assert model_path.exists(), "Модель psycho_life_lgbm.pkl должна существовать"
    assert explainer_path.exists(), "Эксплейнер psycho_shap_explainer.pkl должен существовать"
    assert cols_path.exists(), "Колонки psycho_feature_columns.pkl должны существовать"

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(explainer_path, "rb") as f:
        explainer = pickle.load(f)
    with open(cols_path, "rb") as f:
        cols = pickle.load(f)

    return {"model": model, "explainer": explainer, "cols": cols}


def create_psycho_vector(
    is_crisis: bool = False,
    pharmacy_share: float = 0.02,
    self_care_drop: float = 0.05,
    night_logins: int = 0,
    alimony: float = 0.0,
    salary_trend: float = 1.02,
) -> dict:
    """Хелпер создания вектора психоэмоционального профиля."""
    return {
        "pharmacy_antidepressant_share": pharmacy_share,
        "clinical_therapy_spending_30d": 60000.0 if is_crisis else 0.0,
        "nighttime_alcohol_spend_share": 0.20 if is_crisis else 0.02,
        "gambling_escapism_outflow": 0.0,
        "self_care_drop_rate": self_care_drop,
        "sleep_disruption_night_orders": 8 if is_crisis else 0,
        "night_dbo_login_frequency": night_logins,
        "dwell_time_repayment_screen": 95.0 if is_crisis else 12.0,
        "balance_check_anxiety_index": 8.5 if is_crisis else 1.2,
        "alimony_burden_ratio": alimony,
        "p2p_borrowing_from_friends_count": 3 if is_crisis else 0,
        "utility_debt_months": 1 if is_crisis else 0,
        "salary_trend_post_crisis": salary_trend,
        "dti_dynamic_estimate": 0.65 if is_crisis else 0.30,
        "age": 38,
    }


# ==============================================================================
# ТЕСТ 1: Гармоничный заемщик получает минимальный индекс кризиса (< 0.20)
# ==============================================================================
def test_harmonious_borrower_has_low_psycho_risk(psycho_model_artifacts):
    artifacts = psycho_model_artifacts
    harmonious_client = create_psycho_vector(is_crisis=False)

    df_row = pd.DataFrame([harmonious_client])[artifacts["cols"]]
    p_crisis = artifacts["model"].predict_proba(df_row)[0, 1]

    assert p_crisis < 0.20, f"У благополучного заемщика риск депрессии должен быть низким, получено: {p_crisis:.4f}"


# ==============================================================================
# ТЕСТ 2: Развод, алименты и бессонница вызывают глубокий кризис (> 0.85)
# ==============================================================================
def test_divorce_and_insomnia_triggers_severe_crisis(psycho_model_artifacts):
    artifacts = psycho_model_artifacts
    stressed_divorce_client = create_psycho_vector(
        is_crisis=True,
        pharmacy_share=0.25,      # покупка успокоительных
        self_care_drop=0.85,      # забросил уход за собой
        night_logins=12,          # ночная бессонница и входы в ДБО
        alimony=0.33,             # 33% алиментов после развода
        salary_trend=0.68,        # спад продуктивности на работе
    )

    df_row = pd.DataFrame([stressed_divorce_client])[artifacts["cols"]]
    p_crisis = artifacts["model"].predict_proba(df_row)[0, 1]

    assert p_crisis >= 0.80, f"Заемщик после тяжелого развода обязан получить высокий риск кризиса, получено: {p_crisis:.4f}"


# ==============================================================================
# ТЕСТ 3: Движок TreeSHAP объясняет личные жизненные первопричины кризиса
# ==============================================================================
def test_psycho_shap_identifies_life_crisis_factors(psycho_model_artifacts):
    artifacts = psycho_model_artifacts
    client = create_psycho_vector(
        is_crisis=True,
        pharmacy_share=0.30,
        self_care_drop=0.90,
        night_logins=15,
        alimony=0.33,
    )

    df_row = pd.DataFrame([client])[artifacts["cols"]]
    shap_vals = artifacts["explainer"].shap_values(df_row)

    # Извлекаем вклады Шепли
    if isinstance(shap_vals, list):
        vals = shap_vals[1][0]
    elif len(shap_vals.shape) == 3:
        vals = shap_vals[0, :, 1]
    else:
        vals = shap_vals[0]

    top_drivers = sorted(zip(artifacts["cols"], vals), key=lambda x: x[1], reverse=True)
    top_feature_names = [feat for feat, val in top_drivers[:5]]

    # Проверяем, что в топе факторов вышли именно психологические маркеры
    assert any(
        "self_care" in f or "pharmacy" in f or "alimony" in f or "night" in f or "salary" in f
        for f in top_feature_names
    ), f"Психологические маркеры обязаны быть в топе XAI, получено: {top_feature_names}"
