import pytest
from app.infrastructure.optimization.ortools_restructuring import OrToolsRestructuringOptimizer


@pytest.fixture(scope="module")
def optimizer():
    return OrToolsRestructuringOptimizer()


def test_ortools_finds_viable_scenarios(optimizer):
    """
    Проверка работы математического солвера SCIP для проблемного заемщика:
    Остаток долга: 1 500 000 KZT, ставка 19.5%, срок 24 мес, платеж: 85 000 KZT,
    платежеспособность (free cashflow): 55 000 KZT.
    """
    scenarios = optimizer.optimize(
        client_token="test-client-milp",
        remaining_principal=1500000.0,
        interest_rate=19.5,
        remaining_term_months=24,
        current_monthly_payment=85000.0,
        estimated_client_capacity=55000.0,
    )

    assert len(scenarios) == 3, "OR-Tools обязан сгенерировать ровно 3 альтернативных сценария для клиента"

    for sc in scenarios:
        # Проверяем, что сценарий соответствует нормам регулятора АРРФР
        assert sc.complies_with_arrfr is True, "Каждый план обязан соответствовать требованиям АРРФР"

        # Новый ежемесячный платеж должен быть меньше исходного (85 000 KZT)
        assert sc.new_monthly_payment < 85000.0, f"Платеж {sc.new_monthly_payment} должен быть ниже 85 000 KZT"

        # Восстановление NPV банка
        assert sc.npv_recovery_rate > 0.35, f"Коэффициент возврата долга для банка: {sc.npv_recovery_rate}"


def test_restructuring_scenario_types(optimizer):
    """Проверка разнообразия вариантов предложений для клиента в мобильном банке."""
    scenarios = optimizer.optimize(
        client_token="test-client-types",
        remaining_principal=2500000.0,
        interest_rate=21.0,
        remaining_term_months=36,
        current_monthly_payment=120000.0,
        estimated_client_capacity=80000.0,
    )

    titles = [s.title for s in scenarios]
    assert len(titles) == len(set(titles)), "Все сформированные сценарии должны иметь уникальные заголовки"
    assert any("Пролонгация" in t for t in titles), "Должен присутствовать сценарий пролонгации срока"
    assert any("каникулы" in t.lower() for t in titles), "Должен присутствовать сценарий кредитных каникул"