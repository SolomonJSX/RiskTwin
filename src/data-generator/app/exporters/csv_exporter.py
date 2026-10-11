import pandas as pd
from pathlib import Path
from typing import List
from app.domain.models import SyntheticBorrowerRecord


class CsvDatasetExporter:
    """Экспорт полного датасета в CSV формат."""

    @staticmethod
    def export(records: List[SyntheticBorrowerRecord], file_path: Path) -> pd.DataFrame:
        rows = []
        for r in records:
            p = r.persona
            f = r.features
            row = {
                # PII профиль
                "client_token": p.client_token,
                "full_name": p.full_name,
                "iin": p.iin,
                "age": p.age,
                "gender": p.gender.value,
                "city": p.city,
                "employment_type": p.employment_type.value,
                "industry": p.industry,
                "declared_income": p.declared_income,
                "archetype": p.archetype.value,
                "stress_narrative": p.stress_narrative,
                # 24 финансовых признака
                "salary_trend_ratio_3m_vs_6m": f.salary_trend_ratio_3m_vs_6m,
                "salary_inflow_delay_days": f.salary_inflow_delay_days,
                "inflow_source_entropy": f.inflow_source_entropy,
                "net_cashflow_margin_30d": f.net_cashflow_margin_30d,
                "atm_cash_out_intensity": f.atm_cash_out_intensity,
                "credit_to_debit_transfer_ratio": f.credit_to_debit_transfer_ratio,
                "essential_spending_share_trend": f.essential_spending_share_trend,
                "balance_zero_out_frequency": f.balance_zero_out_frequency,
                "mfo_gambling_tag_presence": 1 if f.mfo_gambling_tag_presence else 0,
                "balance_check_frequency_surge": f.balance_check_frequency_surge,
                "loan_schedule_screen_dwell_time": f.loan_schedule_screen_dwell_time,
                "support_chat_keyword_velocity": f.support_chat_keyword_velocity,
                "microloan_calculator_views": f.microloan_calculator_views,
                "dti_dynamic_estimate": f.dti_dynamic_estimate,
                "active_bnpl_installment_count": f.active_bnpl_installment_count,
                "grace_period_exhaustion_rate": f.grace_period_exhaustion_rate,
                "early_payment_decay_days": f.early_payment_decay_days,
                "median_daily_balance_7d": f.median_daily_balance_7d,
                "median_daily_balance_30d": f.median_daily_balance_30d,
                "median_daily_balance_90d": f.median_daily_balance_90d,
                "p2p_outflow_sum_7d": f.p2p_outflow_sum_7d,
                "p2p_outflow_sum_30d": f.p2p_outflow_sum_30d,
                "failed_autopay_attempts_30d": f.failed_autopay_attempts_30d,
                # Таргеты
                "target_default_30d": r.target_default_30d,
                "predicted_days_to_default": r.predicted_days_to_default,
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        return df