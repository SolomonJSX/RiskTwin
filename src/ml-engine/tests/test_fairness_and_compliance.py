import pytest
from app.domain.entities import ClientFeatureVector
from app.infrastructure.scoring.mock_gradient_boosting import EarlyWarningScoringModel
from app.infrastructure.xai.tree_explainer import ShapExplainabilityEngine


@pytest.fixture(scope="module")
def scoring_model():
    model = EarlyWarningScoringModel()
    assert model._is_loaded
    return model


@pytest.fixture(scope="module")
def xai_engine():
    engine = ShapExplainabilityEngine()
    assert engine._is_loaded
    return engine


def validate_kazakhstan_iin(iin: str) -> bool:
    """Официальный алгоритм валидации контрольного разряда ИИН РК."""
    if len(iin) != 12 or not iin.isdigit():
        return False

    digits = [int(c) for c in iin]
    w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    s1 = sum(d * w for d, w in zip(digits[:11], w1)) % 11
    if s1 < 10:
        return s1 == digits[11]

    w2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
    s2 = sum(d * w for d, w in zip(digits[:11], w2)) % 11
    if s2 < 10:
        return s2 == digits[11]

    return digits[11] == 0


def test_fair_lending_no_pii_bias(scoring_model):
    """
    Требование АРРФР: Модель скоринга не должна использовать
    персональные защищенные атрибуты (пол, имя, город, национальность).
    """
    forbidden_features = {"gender", "sex", "name", "full_name", "city", "iin", "marital_status"}
    used_features = set(scoring_model.feature_cols)

    overlap = forbidden_features.intersection(used_features)
    assert len(overlap) == 0, f"Обнаружены запрещенные признаки дискриминации: {overlap}"


def test_kazakhstan_iin_checksum_validation():
    """Тестирование корректности контрольных сумм казахстанских ИИН."""
    assert validate_kazakhstan_iin("851112370188") is True
    assert validate_kazakhstan_iin("950425425604") is True
    assert validate_kazakhstan_iin("780618324890") is True

    # Искаженные ИИН должны браковаться
    assert validate_kazakhstan_iin("851112370189") is False
    assert validate_kazakhstan_iin("123456789012") is False
    assert validate_kazakhstan_iin("short_iin") is False


def test_bnpl_overleveraged_pattern(scoring_model, xai_engine):
    """Тестирование выявления молодежного паттерна перегруза рассрочками."""
    bnpl_client = ClientFeatureVector(
        client_token="test-bnpl-client",
        salary_trend_ratio_3m_vs_6m=1.0,
        salary_inflow_delay_days=0,
        inflow_source_entropy=1.0,
        net_cashflow_margin_30d=0.08,
        atm_cash_out_intensity=0.15,
        credit_to_debit_transfer_ratio=0.45,
        essential_spending_share_trend=0.88,
        balance_zero_out_frequency=2,
        mfo_gambling_tag_presence=False,
        balance_check_frequency_surge=1.5,
        loan_schedule_screen_dwell_time=25.0,
        support_chat_keyword_velocity=0.0,
        microloan_calculator_views=0,
        dti_dynamic_estimate=0.68,
        active_bnpl_installment_count=6,
        grace_period_exhaustion_rate=0.92,
        early_payment_decay_days=1,
        median_daily_balance_7d=25000.0,
        median_daily_balance_30d=65000.0,
        median_daily_balance_90d=140000.0,
        p2p_outflow_sum_7d=20000.0,
        p2p_outflow_sum_30d=80000.0,
        failed_autopay_attempts_30d=1,
    )

    p_30d, _ = scoring_model.predict_p_default(bnpl_client)
    assert p_30d > 0.40, f"Заемщик с 6 активными BNPL обязан получить повышенный скор: {p_30d}"

    drivers = xai_engine.explain(bnpl_client, top_n=5)
    top_feature_names = [d.feature_name for d in drivers]
    assert any("bnpl" in f or "dti" in f or "balance" in f for f in top_feature_names)