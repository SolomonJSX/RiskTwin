"""
Kaggle Home Credit Default Risk Dataset Preparation.
Downloads real loan applications and real payment transactions (installments).
Aggregates transactional payment behavior (delays, underpayments, cash gaps)
and merges with fundamental credit parameters into a unified dataset.
"""

import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd


def prepare_dataset():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    output_csv = data_dir / "home_credit_transactional_prepared.csv"
    output_parquet = data_dir / "home_credit_transactional_prepared.parquet"

    print("=" * 80)
    print("📥 ПОДГОТОВКА РЕАЛЬНОГО ДАТАСЕТА KAGGLE HOME CREDIT DEFAULT RISK")
    print("=" * 80)

    # 1. Загрузка заявок на кредиты (Application Train)
    app_url = "https://huggingface.co/datasets/mohameddhameem/home-credit-default-risk/resolve/main/application_train_dated/train-00000-of-00001.parquet"
    print(f"[*] Загрузка кредитных анкет и таргета дефолта: {app_url}")
    df_app = pd.read_parquet(app_url)
    print(f"[+] Успешно загружено анкет заемщиков: {len(df_app):,}")

    # 2. Загрузка реальных транзакций платежей (Installments Payments - первый паркет)
    inst_url = "https://huggingface.co/datasets/mohameddhameem/home-credit-default-risk/resolve/main/installments_payments/train-00000-of-00002.parquet"
    print(f"[*] Загрузка реальных платежных транзакций: {inst_url}")
    df_inst = pd.read_parquet(inst_url)
    print(f"[+] Успешно загружено транзакций платежей: {len(df_inst):,}")

    print("\n--- АНАЛИЗ СТРУКТУРЫ ТРАНЗАКЦИЙ ---")
    print(f"Колонки платежей: {list(df_inst.columns)}")

    # 3. Агрегация транзакционного поведения по каждому заемщику
    print("\n⚙️ Расчет транзакционных поведенческих агрегатов...")
    
    # Задержка платежа в днях: положительное число = опоздание с оплатой
    df_inst["payment_delay_days"] = df_inst["DAYS_ENTRY_PAYMENT"] - df_inst["DAYS_INSTALMENT"]
    
    # Флаг просрочки (опоздал хотя бы на 1 день)
    df_inst["is_late_payment"] = (df_inst["payment_delay_days"] > 0).astype(int)

    # Недоплата: уплачено меньше, чем положено по графику
    df_inst["payment_deficit"] = (df_inst["AMT_INSTALMENT"] - df_inst["AMT_PAYMENT"]).clip(lower=0)
    df_inst["is_underpayment"] = (df_inst["payment_deficit"] > 1.0).astype(int)

    # Отношение уплаченного к начисленному
    df_inst["payment_ratio"] = (df_inst["AMT_PAYMENT"] / (df_inst["AMT_INSTALMENT"] + 1e-5)).clip(upper=2.0)

    # Группировка транзакций по заемщику (SK_ID_CURR)
    inst_agg = df_inst.groupby("SK_ID_CURR").agg(
        total_transactions=("NUM_INSTALMENT_NUMBER", "count"),
        avg_payment_delay_days=("payment_delay_days", "mean"),
        max_payment_delay_days=("payment_delay_days", "max"),
        late_payment_count=("is_late_payment", "sum"),
        underpayment_count=("is_underpayment", "sum"),
        avg_payment_ratio=("payment_ratio", "mean"),
        total_payment_deficit=("payment_deficit", "sum"),
        total_amount_paid=("AMT_PAYMENT", "sum"),
    ).reset_index()

    print(f"[+] Транзакции агрегированы для {len(inst_agg):,} заемщиков")

    # 4. Объединение транзакций с анкетой заемщика
    print("\n🔗 Слияние кредитных параметров с транзакционным поведением...")
    merged = pd.merge(df_app, inst_agg, on="SK_ID_CURR", how="inner")
    print(f"[+] Итоговая выборка (заемщики со 100% реальной транзакционной историей): {len(merged):,}")

    # 5. Отбор и расчет чистых ключевых признаков для модели
    merged["dti_ratio"] = merged["AMT_ANNUITY"] / (merged["AMT_INCOME_TOTAL"] + 1e-5)
    merged["credit_to_income_ratio"] = merged["AMT_CREDIT"] / (merged["AMT_INCOME_TOTAL"] + 1e-5)
    merged["age_years"] = (-merged["DAYS_BIRTH"] / 365.25).round(1)
    merged["employment_years"] = (-merged["DAYS_EMPLOYED"] / 365.25).clip(lower=0).round(1)

    selected_columns = [
        "SK_ID_CURR",
        # Таргет дефолта
        "TARGET",
        # Финансовые условия кредита
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "dti_ratio",
        "credit_to_income_ratio",
        # Демография и профиль
        "age_years",
        "employment_years",
        "NAME_CONTRACT_TYPE",
        "NAME_INCOME_TYPE",
        "NAME_HOUSING_TYPE",
        # Поведенческие транзакционные признаки
        "total_transactions",
        "avg_payment_delay_days",
        "max_payment_delay_days",
        "late_payment_count",
        "underpayment_count",
        "avg_payment_ratio",
        "total_payment_deficit",
        "total_amount_paid",
    ]

    final_df = merged[[c for c in selected_columns if c in merged.columns]].copy()

    # Сохраняем и в Parquet (компактно), и в CSV
    print(f"\n💾 Сохранение подготовленного датасета...")
    final_df.to_parquet(output_parquet, index=False)
    # Сохраняем репрезентативную выборку первых 50 000 в CSV для легкого чтения
    sample_csv = final_df.head(50000)
    sample_csv.to_csv(output_csv, index=False)

    print("=" * 80)
    print("🏆 ПОДГОТОВКА ДАТАСЕТА ЗАВЕРШЕНА!")
    print("=" * 80)
    print(f"  🔹 Всего реальных заемщиков с транзакциями : {len(final_df):,}")
    print(f"  🔹 Доля дефолтов (TARGET = 1)              : {final_df['TARGET'].mean():.2%}")
    print(f"  🔹 Число признаков в паспорте             : {len(final_df.columns)}")
    print(f"  🔹 Parquet файл                           : {output_parquet}")
    print(f"  🔹 CSV сэмпл                              : {output_csv}")
    print("=" * 80)
    print("\nПервые 3 строки подготовленного датасета:")
    print(final_df[["SK_ID_CURR", "TARGET", "AMT_INCOME_TOTAL", "AMT_CREDIT", "dti_ratio", "avg_payment_delay_days", "late_payment_count"]].head(3))


if __name__ == "__main__":
    prepare_dataset()
