"""
Full 360-Degree Kaggle Home Credit Dataset Preparation.
Integrates ALL 6 core relational banking tables into a unified borrower passport:
1. application_train (Credit terms, DTI, EXT_SOURCE bureau scores)
2. installments_payments (Payment transaction delays, deficits, cash gaps)
3. POS_CASH_balance (BNPL installments, consumer point-of-sale loans, future debt)
4. credit_card_balance (Credit card ATM cash withdrawals, limits, POS spends)
5. previous_application (Past bank application history, Refused vs Approved)
6. bureau (External credit bureau debts and overdue in other banks)
"""

import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd


BASE_HF_URL = "https://huggingface.co/datasets/mohameddhameem/home-credit-default-risk/resolve/main"


def prepare_full_360():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_parquet = data_dir / "home_credit_full_360_prepared.parquet"
    output_csv = data_dir / "home_credit_full_360_prepared.csv"

    print("=" * 80)
    print("🌐 СБОРКА ПОЛНОГО 360° ДАТАСЕТА ИЗ ВСЕХ 6 ТАБЛИЦ HOME CREDIT")
    print("=" * 80)

    # 1. APPLICATION TRAIN (Базовый кредитный договор и внешние скоры)
    print("\n[1/6] 📥 Загрузка заявок на кредит (application_train)...")
    url_app = f"{BASE_HF_URL}/application_train_dated/train-00000-of-00001.parquet"
    df_app = pd.read_parquet(url_app)
    print(f"      Анкет заемщиков: {len(df_app):,}")

    # Расчет ключевых кредитных коэффициентов
    df_app["dti_ratio"] = df_app["AMT_ANNUITY"] / (df_app["AMT_INCOME_TOTAL"] + 1e-5)
    df_app["credit_to_income_ratio"] = df_app["AMT_CREDIT"] / (df_app["AMT_INCOME_TOTAL"] + 1e-5)
    df_app["age_years"] = (-df_app["DAYS_BIRTH"] / 365.25).round(1)
    df_app["employment_years"] = (-df_app["DAYS_EMPLOYED"] / 365.25).clip(lower=0).round(1)

    # 2. INSTALLMENTS PAYMENTS (Платежные транзакции и задержки)
    print("\n[2/6] 📥 Загрузка и агрегация платежных транзакций (installments_payments)...")
    url_inst = f"{BASE_HF_URL}/installments_payments/train-00000-of-00002.parquet"
    df_inst = pd.read_parquet(url_inst)
    
    df_inst["delay_days"] = df_inst["DAYS_ENTRY_PAYMENT"] - df_inst["DAYS_INSTALMENT"]
    df_inst["is_late"] = (df_inst["delay_days"] > 0).astype(int)
    df_inst["deficit"] = (df_inst["AMT_INSTALMENT"] - df_inst["AMT_PAYMENT"]).clip(lower=0)
    df_inst["is_underpay"] = (df_inst["deficit"] > 1.0).astype(int)

    agg_inst = df_inst.groupby("SK_ID_CURR").agg(
        inst_total_tx=("NUM_INSTALMENT_NUMBER", "count"),
        inst_avg_delay_days=("delay_days", "mean"),
        inst_max_delay_days=("delay_days", "max"),
        inst_late_count=("is_late", "sum"),
        inst_underpay_count=("is_underpay", "sum"),
        inst_total_deficit=("deficit", "sum"),
    ).reset_index()
    print(f"      Агрегировано по {len(agg_inst):,} заемщикам")

    # 3. POS CASH BALANCE (Товарные рассрочки, Kaspi Red аналог, BNPL)
    print("\n[3/6] 📥 Загрузка и агрегация товарных рассрочек (POS_CASH_balance)...")
    url_pos = f"{BASE_HF_URL}/POS_CASH_balance/train-00000-of-00002.parquet"
    df_pos = pd.read_parquet(url_pos)

    df_pos["is_active"] = (df_pos["NAME_CONTRACT_STATUS"] == "Active").astype(int)
    df_pos["is_completed"] = (df_pos["NAME_CONTRACT_STATUS"] == "Completed").astype(int)

    agg_pos = df_pos.groupby("SK_ID_CURR").agg(
        pos_active_count=("is_active", "sum"),
        pos_completed_count=("is_completed", "sum"),
        pos_remaining_installments=("CNT_INSTALMENT_FUTURE", "mean"),
        pos_max_dpd=("SK_DPD", "max"),
    ).reset_index()
    print(f"      Агрегировано по {len(agg_pos):,} заемщикам")

    # 4. CREDIT CARD BALANCE (Кредитки: банкоматы, снятие наличных, лимиты)
    print("\n[4/6] 📥 Загрузка выписок по кредитным картам (credit_card_balance)...")
    url_cc = f"{BASE_HF_URL}/credit_card_balance/train-00000-of-00002.parquet"
    df_cc = pd.read_parquet(url_cc)

    df_cc["cc_utilization"] = (df_cc["AMT_BALANCE"] / (df_cc["AMT_CREDIT_LIMIT_ACTUAL"] + 1e-5)).clip(0, 2)

    agg_cc = df_cc.groupby("SK_ID_CURR").agg(
        cc_atm_drawings_sum=("AMT_DRAWINGS_ATM_CURRENT", "sum"),
        cc_atm_drawings_cnt=("CNT_DRAWINGS_ATM_CURRENT", "sum"),
        cc_pos_drawings_sum=("AMT_DRAWINGS_POS_CURRENT", "sum"),
        cc_utilization_mean=("cc_utilization", "mean"),
        cc_max_dpd=("SK_DPD", "max"),
    ).reset_index()
    print(f"      Агрегировано по {len(agg_cc):,} заемщикам")

    # 5. PREVIOUS APPLICATION (История прошлых заявок: отказы vs одобрения)
    print("\n[5/6] 📥 Загрузка истории прошлых заявок (previous_application)...")
    url_prev = f"{BASE_HF_URL}/previous_application/train-00000-of-00002.parquet"
    df_prev = pd.read_parquet(url_prev)

    df_prev["is_refused"] = (df_prev["NAME_CONTRACT_STATUS"] == "Refused").astype(int)
    df_prev["is_approved"] = (df_prev["NAME_CONTRACT_STATUS"] == "Approved").astype(int)

    agg_prev = df_prev.groupby("SK_ID_CURR").agg(
        prev_app_total=("SK_ID_PREV", "count"),
        prev_refused_count=("is_refused", "sum"),
        prev_approved_count=("is_approved", "sum"),
    ).reset_index()
    print(f"      Агрегировано по {len(agg_prev):,} заемщикам")

    # 6. BUREAU (Кредиты в ДРУГИХ банках страны — ПКБ)
    print("\n[6/6] 📥 Загрузка кредитов в сторонних банках (bureau)...")
    url_bureau = f"{BASE_HF_URL}/bureau/train-00000-of-00001.parquet"
    df_bureau = pd.read_parquet(url_bureau)

    df_bureau["is_active"] = (df_bureau["CREDIT_ACTIVE"] == "Active").astype(int)

    agg_bureau = df_bureau.groupby("SK_ID_CURR").agg(
        bureau_active_loans=("is_active", "sum"),
        bureau_total_debt=("AMT_CREDIT_SUM_DEBT", "sum"),
        bureau_total_overdue=("AMT_CREDIT_SUM_OVERDUE", "sum"),
        bureau_prolong_count=("CNT_CREDIT_PROLONG", "sum"),
    ).reset_index()
    print(f"      Агрегировано по {len(agg_bureau):,} заемщикам")

    # 7. Единое слияние всех 6 доменов в 360-градусный паспорт
    print("\n🔗 Слияние всех 6 доменов воедино...")
    merged = df_app.merge(agg_inst, on="SK_ID_CURR", how="inner")
    merged = merged.merge(agg_pos, on="SK_ID_CURR", how="left")
    merged = merged.merge(agg_cc, on="SK_ID_CURR", how="left")
    merged = merged.merge(agg_prev, on="SK_ID_CURR", how="left")
    merged = merged.merge(agg_bureau, on="SK_ID_CURR", how="left")

    # Заполнение пропусков для клиентов без кредиток / бюро нулями
    fill_zero_cols = [
        "pos_active_count", "pos_completed_count", "pos_remaining_installments", "pos_max_dpd",
        "cc_atm_drawings_sum", "cc_atm_drawings_cnt", "cc_pos_drawings_sum", "cc_utilization_mean", "cc_max_dpd",
        "prev_app_total", "prev_refused_count", "prev_approved_count",
        "bureau_active_loans", "bureau_total_debt", "bureau_total_overdue", "bureau_prolong_count",
        "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
    ]
    for col in fill_zero_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    selected_360_cols = [
        "SK_ID_CURR",
        "TARGET",
        # 1. Кредитный договор и профиль
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "dti_ratio",
        "credit_to_income_ratio",
        "age_years",
        "employment_years",
        "NAME_CONTRACT_TYPE",
        "NAME_INCOME_TYPE",
        "NAME_HOUSING_TYPE",
        # 2. Внешние скоры ПКБ
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3",
        # 3. Платежные транзакции
        "inst_total_tx",
        "inst_avg_delay_days",
        "inst_max_delay_days",
        "inst_late_count",
        "inst_underpay_count",
        "inst_total_deficit",
        # 4. Товарные рассрочки POS / BNPL
        "pos_active_count",
        "pos_completed_count",
        "pos_remaining_installments",
        "pos_max_dpd",
        # 5. Кредитные карты (банкоматы и покупки)
        "cc_atm_drawings_sum",
        "cc_atm_drawings_cnt",
        "cc_pos_drawings_sum",
        "cc_utilization_mean",
        "cc_max_dpd",
        # 6. Прошлые отказы банка
        "prev_app_total",
        "prev_refused_count",
        "prev_approved_count",
        # 7. Долги в других банках (внешнее бюро)
        "bureau_active_loans",
        "bureau_total_debt",
        "bureau_total_overdue",
        "bureau_prolong_count",
    ]

    final_360 = merged[[c for c in selected_360_cols if c in merged.columns]].copy()

    # Сохранение
    print(f"\n💾 Сохранение единого 360° датасета...")
    final_360.to_parquet(output_parquet, index=False)
    final_360.head(50000).to_csv(output_csv, index=False)

    print("=" * 80)
    print("🏆 ПОЛНЫЙ 360° ДАТАСЕТ ИЗ 6 ТАБЛИЦ УСПЕШНО СОБРАН!")
    print("=" * 80)
    print(f"  🔹 Всего заемщиков в 360° паспорте : {len(final_360):,}")
    print(f"  🔹 Доля дефолтов                   : {final_360['TARGET'].mean():.2%}")
    print(f"  🔹 Итоговое число признаков        : {len(final_360.columns)}")
    print(f"  🔹 Parquet файл                    : {output_parquet}")
    print(f"  🔹 CSV сэмпл                       : {output_csv}")
    print("=" * 80)
    print("\nПример профиля (первая строка):")
    for col in final_360.columns[:15]:
        print(f"  • {col:<26}: {final_360[col].iloc[0]}")


if __name__ == "__main__":
    prepare_full_360()
