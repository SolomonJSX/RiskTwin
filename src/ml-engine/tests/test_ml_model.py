import pytest
import numpy as np
from app.domain.entities import ClientFeatureVector
from app.infrastructure.scoring.mock_gradient_boosting import EarlyWarningScoringModel
from app.infrastructure.xai.tree_explainer import ShapExplainabilityEngine
from app.infrastructure.optimization.ortools_restructuring import OrToolsRestructuringOptimizer


@pytest.fixture(scope="module")
def scoring_model():
    model = EarlyWarningScoringModel()
    assert model._is_loaded, "LightGBM модель должна быть успешно загружена из models/early_warning_lgbm.pkl"
    return model


@pytest.fixture(scope="module")
def xai_engine():
    engine = ShapExplainabilityEngine()
    assert engine._is_loaded, "SHAP Explainer должен быть успешно загружен из models/shap_explainer.pkl"
    return engine


@pytest.fixture(scope="module")
def restructuring_optimizer():
    return OrToolsRestructuringOptimizer()


def create_sample_vector(
    salary_trend: float = 1.0,
    mfo_presence: bool = False,
    dti: float = 0.30,
    bnpl_count: int = 1,
    failed_autopay: int = 0,
    zero_out_days: int = 1,
) -> ClientFeatureVector:
    """Хелпер создания реалистичного вектора признаков заемщика."""
    return ClientFeatureVector(
        client_token="test-token-0001",
        salary_trend_ratio_3m_vs_6m=salary_trend,
        salary_inflow_delay_days=1 if salary_trend >= 0.9 else 12,
        inflow_source_entropy=1.1 if not mfo_presence else 2.8,
        net_cashflow_margin_30d=0.20 if salary_trend >= 0.9 else -0.25,
        atm_cash_out_intensity=0.20 if not mfo_presence else 0.65,
        credit_to_debit_transfer_ratio=0.10 if not mfo_presence else 0.55,
        essential_spending_share_trend=0.50 if salary_trend >= 0.9 else 0.90,
        balance_zero_out_frequency=zero_out_days,
        mfo_gambling_tag_presence=mfo_presence,
        balance_check_frequency_surge=1.0 if salary_trend >= 0.9 else 3.8,
        loan_schedule_screen_dwell_time=15.0 if salary_trend >= 0.9 else 95.0,
        support_chat_keyword_velocity=0.0 if not mfo_presence else 2.5,
        microloan_calculator_views=0 if not mfo_presence else 3,
        dti_dynamic_estimate=dti,
        active_bnpl_installment_count=bnpl_count,
        grace_period_exhaustion_rate=0.10 if bnpl_count <= 2 else 0.90,
        early_payment_decay_days=0 if salary_trend >= 0.9 else 1,
        median_daily_balance_7d=150000.0 if salary_trend >= 0.9 else 12000.0,
        median_daily_balance_30d=160000.0 if salary_trend >= 0.9 else 25000.0,
        median_daily_balance_90d=170000.0,
        p2p_outflow_sum_7d=30000.0,
        p2p_outflow_sum_30d=120000.0,
        failed_autopay_attempts_30d=failed_autopay,
    )


# ==============================================================================
# ТЕСТ 1: Baseline Sanity (Идеальный клиент не должен получать преддефолт)
# ==============================================================================
def test_healthy_borrower_has_low_risk(scoring_model):
    healthy_client = create_sample_vector(
        salary_trend=1.02,
        mfo_presence=False,
        dti=0.25,
        bnpl_count=0,
        failed_autopay=0,
    )
    p_30d, p_60d = scoring_model.predict_p_default(healthy_client)

    assert 0.0 <= p_30d <= 1.0, "Вероятность должна лежать в диапазоне [0, 1]"
    assert p_30d < 0.25, f"У идеального заемщика скор должен быть низким, получено: {p_30d}"
    assert p_60d >= p_30d, "Риск на горизонте 60 дней должен быть не ниже риска на 30 дней"


# ==============================================================================
# ТЕСТ 2: Stress Sensitivity (При падении зарплаты и МФО риск обязан вырасти)
# ==============================================================================
def test_monotonic_risk_increase_under_stress(scoring_model):
    healthy_client = create_sample_vector(salary_trend=1.0, mfo_presence=False, dti=0.28)
    stressed_client = create_sample_vector(salary_trend=0.55, mfo_presence=True, dti=0.68)

    p_healthy_30d, _ = scoring_model.predict_p_default(healthy_client)
    p_stressed_30d, _ = scoring_model.predict_p_default(stressed_client)

    delta = p_stressed_30d - p_healthy_30d
    assert delta > 0.40, f"При стрессе риск должен вырасти минимум на 40 п.п., дельта: {delta:.2f}"
    assert p_stressed_30d >= 0.60, f"Преддефолтный клиент должен получить высокий скор, получено: {p_stressed_30d}"


# ==============================================================================
# ТЕСТ 3: SHAP Interpretability Consistency (Факторы XAI должны объяснять причину)
# ==============================================================================
def test_shap_factors_reflect_true_cause(xai_engine):
    mfo_client = create_sample_vector(
        salary_trend=0.95,
        mfo_presence=True,
        dti=0.75,
        failed_autopay=3,
    )
    drivers = xai_engine.explain(mfo_client, top_n=5)

    assert len(drivers) > 0, "Движок SHAP должен вернуть ключевые драйверы"
    top_feature_names = [d.feature_name for d in drivers]

    assert any("mfo" in name or "autopay" in name for name in top_feature_names), (
        f"Драйверы МФО/автоплатежей должны быть в топе XAI, получено: {top_feature_names}"
    )

    for d in drivers:
        assert len(d.human_readable_reason) > 10, f"Поле human_readable_reason должно быть заполнено: {d}"


# ==============================================================================
# ТЕСТ 4: Детерминированность инференса (Отсутствие случайных блужданий)
# ==============================================================================
def test_inference_is_strictly_deterministic(scoring_model):
    client = create_sample_vector(salary_trend=0.88, dti=0.45)
    p1_30, p1_60 = scoring_model.predict_p_default(client)
    p2_30, p2_60 = scoring_model.predict_p_default(client)

    assert p1_30 == p2_30, "Инференс обязан быть абсолютно детерминированным"
    assert p1_60 == p2_60


# ==============================================================================
# ТЕСТ 5: Граничные стресс-тесты (Edge Cases & No NaN/Overflow)
# ==============================================================================
@pytest.mark.parametrize("extreme_salary,extreme_dti,extreme_zero_days", [
    (0.0, 2.5, 0),
    (1.5, 0.05, 12),
    (0.5, 1.0, 50),
])
def test_edge_cases_no_nan_or_overflow(scoring_model, extreme_salary, extreme_dti, extreme_zero_days):
    client = create_sample_vector(
        salary_trend=extreme_salary,
        dti=extreme_dti,
        zero_out_days=extreme_zero_days,
    )
    p_30d, p_60d = scoring_model.predict_p_default(client)

    assert not np.isnan(p_30d) and not np.isnan(p_60d)
    assert 0.0 <= p_30d <= 1.0
    assert 0.0 <= p_60d <= 1.0


# ==============================================================================
# ТЕСТ 6: Регуляторная нейтральность (Отсутствие PII признаков и скрытого Bias)
# ==============================================================================
def test_fair_lending_no_pii_features_in_model(scoring_model):
    """
    Требование АРРФР: Модель скоринга не имеет права использовать
    ФИО, пол, национальность, город или семейное положение.
    """
    forbidden_features = {"gender", "sex", "name", "full_name", "city", "iin", "marital_status"}
    used_features = set(scoring_model.feature_cols)

    overlap = forbidden_features.intersection(used_features)
    assert len(overlap) == 0, f"Нарушение регламента справедливого кредитования! Найдены запрещенные фичи: {overlap}"


# ==============================================================================
# ТЕСТ 7: Выявление молодежного паттерна BNPL Overleveraging (Рассрочки 0-0-24)
# ==============================================================================
def test_bnpl_overleveraged_archetype_detection(scoring_model, xai_engine):
    """
    Заемщик со стабильной зарплатой, но накопивший 7 параллельных рассрочек BNPL.
    Модель должна зафиксировать повышенный риск, а SHAP показать BNPL в факторах.
    """
    bnpl_client = create_sample_vector(
        salary_trend=1.0,
        mfo_presence=False,
        dti=0.68,
        bnpl_count=7,
        failed_autopay=1,
    )
    p_30d, _ = scoring_model.predict_p_default(bnpl_client)

    assert p_30d > 0.45, f"Заемщик с 7 активными BNPL должен получить повышенный скор риска, получено: {p_30d}"

    drivers = xai_engine.explain(bnpl_client, top_n=5)
    top_feature_names = [d.feature_name for d in drivers]
    assert any("bnpl" in name or "dti" in name or "autopay" in name for name in top_feature_names), (
        f"BNPL или DTI должны быть в числе главных драйверов риска, получено: {top_feature_names}"
    )


# ==============================================================================
# ТЕСТ 8: Кумулятивная инвариантность временного горизонта (P_60d >= P_30d)
# ==============================================================================
def test_survival_monotonicity_across_diverse_portfolio(scoring_model):
    """
    Для любого профиля заемщика кумулятивный риск на 60 днях
    математически не может быть меньше риска на 30 днях.
    """
    np.random.seed(123)
    for _ in range(50):
        rand_salary = float(np.random.uniform(0.3, 1.3))
        rand_dti = float(np.random.uniform(0.1, 0.9))
        rand_mfo = bool(np.random.choice([True, False]))

        client = create_sample_vector(salary_trend=rand_salary, mfo_presence=rand_mfo, dti=rand_dti)
        p_30d, p_60d = scoring_model.predict_p_default(client)

        assert p_60d >= p_30d, f"Нарушение монотонности горизонта: p_30d={p_30d}, p_60d={p_60d}"