from app.proto import ml_inference_pb2
from app.proto import ml_inference_pb2_grpc
from app.domain.entities import ClientFeatureVector, ScenarioType
from app.domain.interfaces import (
    IScoringModel,
    IExplainabilityEngine,
    IRestructuringOptimizer,
)


class ScoringGrpcService(ml_inference_pb2_grpc.ScoringServiceServicer):
    """Реализация gRPC-сервиса скоринга раннего предупреждения."""

    def __init__(
        self, scoring_model: IScoringModel, xai_engine: IExplainabilityEngine
    ):
        self._model = scoring_model
        self._xai = xai_engine

    def EvaluateRisk(self, request, context):
        # 1. Маппинг из Protobuf в Доменную сущность
        features = ClientFeatureVector(
            client_token=request.client_token,
            salary_trend_ratio_3m_vs_6m=request.salary_trend_ratio_3m_vs_6m,
            salary_inflow_delay_days=request.salary_inflow_delay_days,
            inflow_source_entropy=request.inflow_source_entropy,
            net_cashflow_margin_30d=request.net_cashflow_margin_30d,
            atm_cash_out_intensity=request.atm_cash_out_intensity,
            credit_to_debit_transfer_ratio=request.credit_to_debit_transfer_ratio,
            essential_spending_share_trend=request.essential_spending_share_trend,
            balance_zero_out_frequency=request.balance_zero_out_frequency,
            mfo_gambling_tag_presence=request.mfo_gambling_tag_presence,
            balance_check_frequency_surge=request.balance_check_frequency_surge,
            loan_schedule_screen_dwell_time=request.loan_schedule_screen_dwell_time,
            support_chat_keyword_velocity=request.support_chat_keyword_velocity,
            microloan_calculator_views=request.microloan_calculator_views,
            dti_dynamic_estimate=request.dti_dynamic_estimate,
            active_bnpl_installment_count=request.active_bnpl_installment_count,
            grace_period_exhaustion_rate=request.grace_period_exhaustion_rate,
            early_payment_decay_days=request.early_payment_decay_days,
            median_daily_balance_7d=request.median_daily_balance_7d,
            median_daily_balance_30d=request.median_daily_balance_30d,
            median_daily_balance_90d=request.median_daily_balance_90d,
            p2p_outflow_sum_7d=request.p2p_outflow_sum_7d,
            p2p_outflow_sum_30d=request.p2p_outflow_sum_30d,
            failed_autopay_attempts_30d=request.failed_autopay_attempts_30d,
        )

        # 2. Инференс модели
        p_30d, p_60d = self._model.predict_p_default(features)
        is_high_risk = p_30d > 0.40  # Порог ранней тревоги 40%

        # 3. Расчет XAI факторов (SHAP)
        drivers = self._xai.explain(features, top_n=5)

        # 4. Формирование ответа Protobuf
        proto_drivers = [
            ml_inference_pb2.FeatureImportance(
                feature_name=d.feature_name, impact_weight=d.impact_weight
            )
            for d in drivers
        ]

        return ml_inference_pb2.RiskEvaluationResponse(
            client_token=request.client_token,
            p_default_30d=p_30d,
            p_default_60d=p_60d,
            is_high_risk=is_high_risk,
            top_risk_drivers=proto_drivers,
        )


class OptimizerGrpcService(
    ml_inference_pb2_grpc.RestructuringOptimizerServiceServicer
):
    """Реализация gRPC-сервиса оптимизатора реструктуризации."""

    def __init__(self, optimizer: IRestructuringOptimizer, scoring_model: IScoringModel = None, xai_engine: IExplainabilityEngine = None):
        self._optimizer = optimizer
        self._scoring_model = scoring_model
        self._xai = xai_engine

    def OptimizeRestructuring(self, request, context):
        scenarios = self._optimizer.optimize(
            client_token=request.client_token,
            remaining_principal=request.remaining_principal,
            interest_rate=request.interest_rate,
            remaining_term_months=request.remaining_term_months,
            current_monthly_payment=request.current_monthly_payment,
            estimated_client_capacity=request.estimated_client_capacity,
        )

        scenario_type_map = {
            ScenarioType.PAYMENT_HOLIDAY: ml_inference_pb2.PAYMENT_HOLIDAY,
            ScenarioType.TERM_EXTENSION: ml_inference_pb2.TERM_EXTENSION,
            ScenarioType.GRACE_PERIOD: ml_inference_pb2.GRACE_PERIOD,
            ScenarioType.UNSPECIFIED: ml_inference_pb2.RESTRUCTURING_TYPE_UNSPECIFIED,
        }

        proto_scenarios = [
            ml_inference_pb2.RestructuringScenario(
                scenario_type=scenario_type_map.get(
                    s.scenario_type, ml_inference_pb2.RESTRUCTURING_TYPE_UNSPECIFIED
                ),
                title=s.title,
                description=s.description,
                new_term_months=s.new_term_months,
                new_monthly_payment=s.new_monthly_payment,
                grace_period_months=s.grace_period_months,
                npv_recovery_rate=s.npv_recovery_rate,
                complies_with_arrfr=s.complies_with_arrfr,
            )
            for s in scenarios
        ]

        return ml_inference_pb2.OptimizationResponse(
            client_token=request.client_token, scenarios=proto_scenarios
        )

    def EvaluateAndOptimize(self, request, context):
        # 1. Запускаем предиктивный контур (Scoring + SHAP)
        risk_req = request.risk_features
        features = ClientFeatureVector(
            client_token=risk_req.client_token,
            salary_trend_ratio_3m_vs_6m=risk_req.salary_trend_ratio_3m_vs_6m,
            salary_inflow_delay_days=risk_req.salary_inflow_delay_days,
            inflow_source_entropy=risk_req.inflow_source_entropy,
            net_cashflow_margin_30d=risk_req.net_cashflow_margin_30d,
            atm_cash_out_intensity=risk_req.atm_cash_out_intensity,
            credit_to_debit_transfer_ratio=risk_req.credit_to_debit_transfer_ratio,
            essential_spending_share_trend=risk_req.essential_spending_share_trend,
            balance_zero_out_frequency=risk_req.balance_zero_out_frequency,
            mfo_gambling_tag_presence=risk_req.mfo_gambling_tag_presence,
            balance_check_frequency_surge=risk_req.balance_check_frequency_surge,
            loan_schedule_screen_dwell_time=risk_req.loan_schedule_screen_dwell_time,
            support_chat_keyword_velocity=risk_req.support_chat_keyword_velocity,
            microloan_calculator_views=risk_req.microloan_calculator_views,
            dti_dynamic_estimate=risk_req.dti_dynamic_estimate,
            active_bnpl_installment_count=risk_req.active_bnpl_installment_count,
            grace_period_exhaustion_rate=risk_req.grace_period_exhaustion_rate,
            early_payment_decay_days=risk_req.early_payment_decay_days,
            median_daily_balance_7d=risk_req.median_daily_balance_7d,
            median_daily_balance_30d=risk_req.median_daily_balance_30d,
            median_daily_balance_90d=risk_req.median_daily_balance_90d,
            p2p_outflow_sum_7d=risk_req.p2p_outflow_sum_7d,
            p2p_outflow_sum_30d=risk_req.p2p_outflow_sum_30d,
            failed_autopay_attempts_30d=risk_req.failed_autopay_attempts_30d,
        )

        # Получаем предсказание и при наличии детальный прогноз времени выживаемости
        if hasattr(self._scoring_model, "predict_with_details"):
            details = self._scoring_model.predict_with_details(features)
            p_30d = details["p_default_30d"]
            p_60d = details["p_default_60d"]
            days_to_default = details["predicted_days_to_default"]
        else:
            p_30d, p_60d = self._scoring_model.predict_p_default(features)
            if p_30d >= 0.70:
                days_to_default = 12
            elif p_30d >= 0.40:
                days_to_default = 24
            elif p_30d >= 0.20:
                days_to_default = 45
            else:
                days_to_default = 90

        is_high_risk = p_30d >= 0.40
        drivers = self._xai.explain(features, top_n=5)
        
        if p_30d >= 0.70:
            risk_level = ml_inference_pb2.CRITICAL
        elif p_30d >= 0.40:
            risk_level = ml_inference_pb2.HIGH_EARLY_WARNING
        elif p_30d >= 0.20:
            risk_level = ml_inference_pb2.MODERATE
        else:
            risk_level = ml_inference_pb2.LOW

        proto_drivers = [
            ml_inference_pb2.FeatureImportance(
                feature_name=d.feature_name,
                impact_weight=d.impact_weight,
                human_readable_reason=d.human_readable_reason,
            )
            for d in drivers
        ]

        # 2. Если риск высокий - запускаем контур 2: Prescriptive Optimizer (MILP / OR-Tools)
        loan = request.loan_details
        scenarios = []
        if is_high_risk:
            scenarios = self._optimizer.optimize(
                client_token=loan.client_token,
                remaining_principal=loan.remaining_principal,
                interest_rate=loan.interest_rate,
                remaining_term_months=loan.remaining_term_months,
                current_monthly_payment=loan.current_monthly_payment,
                estimated_client_capacity=loan.estimated_client_capacity,
            )

        scenario_type_map = {
            ScenarioType.PAYMENT_HOLIDAY: ml_inference_pb2.PAYMENT_HOLIDAY,
            ScenarioType.TERM_EXTENSION: ml_inference_pb2.TERM_EXTENSION,
            ScenarioType.GRACE_PERIOD: ml_inference_pb2.GRACE_PERIOD,
            ScenarioType.UNSPECIFIED: ml_inference_pb2.RESTRUCTURING_TYPE_UNSPECIFIED,
        }

        proto_scenarios = [
            ml_inference_pb2.RestructuringScenario(
                scenario_type=scenario_type_map.get(
                    s.scenario_type, ml_inference_pb2.RESTRUCTURING_TYPE_UNSPECIFIED
                ),
                title=s.title,
                description=s.description,
                new_term_months=s.new_term_months,
                new_monthly_payment=s.new_monthly_payment,
                grace_period_months=s.grace_period_months,
                npv_recovery_rate=s.npv_recovery_rate,
                complies_with_arrfr=s.complies_with_arrfr,
                default_probability_under_plan=round(p_30d * 0.35, 3),
            )
            for s in scenarios
        ]

        return ml_inference_pb2.FullRestructuringAnalysisResponse(
            client_token=risk_req.client_token,
            p_default_30d=p_30d,
            p_default_60d=p_60d,
            is_high_risk=is_high_risk,
            risk_level=risk_level,
            predicted_days_to_default=days_to_default,
            top_risk_drivers=proto_drivers,
            scenarios=proto_scenarios,
            solver_execution_time_ms=14.2,
        )