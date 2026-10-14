"""
Unit & Integration Tests for the Data-Driven Behavioral Distress Engine.
Verifies that behavioral distress is detected solely from objective dataset features
without any hardcoded artificial heuristics.
"""

import pytest
import numpy as np
from app.domain.behavioral_distress import BehavioralDistressEngine
from app.domain.entities import ClientFeatureVector


@pytest.fixture(scope="module")
def distress_engine():
    engine = BehavioralDistressEngine()
    assert engine._is_loaded, "BehavioralDistressEngine должен успешно загружать обученные артефакты GMM"
    return engine


def test_engine_loads_unsupervised_artifacts(distress_engine):
    """Проверяет корректность загрузки артефактов GMM и скалера."""
    assert len(distress_engine.feature_names) == 6
    assert len(distress_engine.cluster_mapping) == 4
    assert len(distress_engine.sorted_order) == 4
    assert "cash_panic_ratio" in distress_engine.feature_names
    assert "payment_delay_distress" in distress_engine.feature_names


def test_disciplined_borrower_has_low_distress(distress_engine):
    """
    Проверяет, что заемщик со стабильным финансовым поведением
    классифицируется в кластер финансовой устойчивости с минимальным скором стресса.
    """
    calm_vector = ClientFeatureVector(
        client_token="test-calm-borrower",
        salary_trend_ratio_3m_vs_6m=1.05,
        salary_inflow_delay_days=0,
        inflow_source_entropy=0.1,
        net_cashflow_margin_30d=0.35,
        atm_cash_out_intensity=0.08,
        credit_to_debit_transfer_ratio=0.0,
        essential_spending_share_trend=0.3,
        balance_zero_out_frequency=0,
        mfo_gambling_tag_presence=False,
        balance_check_frequency_surge=1.0,
        loan_schedule_screen_dwell_time=12.0,
        support_chat_keyword_velocity=0.0,
        microloan_calculator_views=0,
        dti_dynamic_estimate=0.25,
        active_bnpl_installment_count=0,
        grace_period_exhaustion_rate=0.0,
        early_payment_decay_days=0,
        median_daily_balance_7d=450000.0,
        median_daily_balance_30d=420000.0,
        median_daily_balance_90d=400000.0,
        p2p_outflow_sum_7d=20000.0,
        p2p_outflow_sum_30d=80000.0,
        failed_autopay_attempts_30d=0,
    )

    result = distress_engine.evaluate_distress(calm_vector)
    
    assert result["cluster_code"] == "STABLE_DISCIPLINE", f"Ожидался STABLE_DISCIPLINE, получено: {result['cluster_code']}"
    assert result["risk_level"] == "LOW"
    assert result["distress_score"] < 0.25, f"Скор стресса спокойного заемщика должен быть < 0.25, получено: {result['distress_score']}"
    assert result["default_rate_benchmark"] < 0.085


def test_acute_cash_panic_borrower_detection(distress_engine):
    """
    Проверяет выявление острой паники: снятие наличных в банкоматах с кредиток,
    исчерпание грейс-периода и веерные отказы.
    """
    panic_vector = ClientFeatureVector(
        client_token="test-panic-borrower",
        salary_trend_ratio_3m_vs_6m=0.72,
        salary_inflow_delay_days=5,
        inflow_source_entropy=0.6,
        net_cashflow_margin_30d=-0.2,
        atm_cash_out_intensity=0.85,
        credit_to_debit_transfer_ratio=0.75,
        essential_spending_share_trend=0.8,
        balance_zero_out_frequency=8,
        mfo_gambling_tag_presence=True,
        balance_check_frequency_surge=4.5,
        loan_schedule_screen_dwell_time=95.0,
        support_chat_keyword_velocity=0.8,
        microloan_calculator_views=4,
        dti_dynamic_estimate=0.75,
        active_bnpl_installment_count=3,
        grace_period_exhaustion_rate=1.0,
        early_payment_decay_days=8,
        median_daily_balance_7d=15000.0,
        median_daily_balance_30d=45000.0,
        median_daily_balance_90d=150000.0,
        p2p_outflow_sum_7d=180000.0,
        p2p_outflow_sum_30d=420000.0,
        failed_autopay_attempts_30d=3,
    )

    result = distress_engine.evaluate_distress(panic_vector)
    
    # Должен попасть в кластер повышенного стресса / паники
    assert result["cluster_code"] in ["ACUTE_PANIC", "CHRONIC_EXHAUSTION", "LATENT_ANXIETY"]
    assert result["distress_score"] >= 0.50, f"Скор стресса заемщика в панике должен быть >= 0.50, получено: {result['distress_score']}"
    
    # Проверяем, что в ключевых драйверах объективные факторы датасета
    top_driver_names = [d["feature"] for d in result["top_distress_drivers"]]
    assert any(f in top_driver_names for f in ["cash_panic_ratio", "rejection_desperation_rate", "deficit_burden_ratio"])


def test_home_credit_raw_dataset_mapping(distress_engine):
    """
    Проверяет, что движок напрямую обрабатывает сырые строки из датасета Home Credit (163 517 строк).
    """
    raw_home_credit_row = {
        "cc_atm_drawings_sum": 150000.0,
        "cc_pos_drawings_sum": 10000.0,
        "cc_utilization_mean": 0.95,
        "inst_avg_delay_days": 18.5,
        "inst_total_tx": 24,
        "inst_late_count": 8,
        "AMT_ANNUITY": 45000.0,
        "inst_total_deficit": 90000.0,
        "prev_app_total": 5,
        "prev_refused_count": 3,
        "pos_active_count": 4,
        "pos_remaining_installments": 10.0,
        "bureau_total_overdue": 50000.0,
        "pos_max_dpd": 15.0,
        "cc_max_dpd": 0.0,
    }

    result = distress_engine.evaluate_distress(raw_home_credit_row)
    
    assert result["distress_score"] > 0.40
    assert result["cluster_code"] in ["ACUTE_PANIC", "CHRONIC_EXHAUSTION"]
    assert len(result["top_distress_drivers"]) > 0
