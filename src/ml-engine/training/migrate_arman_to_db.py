"""
Скрипт переноса полной истории Армана (все 7 CSV-файлов + профили) в базу данных PostgreSQL (risktwin_db).
"""

import sys
import os
import json
import subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import pandas as pd

def migrate_to_postgres():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data" / "arman_history"
    sql_file = data_dir / "migrate_arman.sql"

    print("=" * 80)
    print("🐘 МИГРАЦИЯ ИСТОРИИ АРМАНА В POSTGRESQL (risktwin_db)")
    print(f"📁 Источник CSV: {data_dir}")
    print("=" * 80)

    # Загружаем CSV
    df_app = pd.read_csv(data_dir / "arman_application.csv")
    df_inst = pd.read_csv(data_dir / "arman_installments_payments.csv")
    df_pos = pd.read_csv(data_dir / "arman_pos_cash_balance.csv")
    df_cc = pd.read_csv(data_dir / "arman_credit_card_balance.csv")
    df_prev = pd.read_csv(data_dir / "arman_previous_application.csv")
    df_bureau = pd.read_csv(data_dir / "arman_bureau.csv")
    df_tx = pd.read_csv(data_dir / "arman_bank_statement_transactions.csv")
    df_telem = pd.read_csv(data_dir / "arman_telemetry_stream.csv")

    sql_statements = []

    # 1. UPSERT В ACCOUNTS
    sql_statements.append("""
-- 1. accounts
INSERT INTO accounts (client_token, segment, current_kdn, is_restructuring_active, created_at)
VALUES ('11111111-2222-3333-4444-555555555555', 'TECH_PREMIUM', 0.12, false, NOW())
ON CONFLICT (client_token) DO UPDATE 
SET segment = 'TECH_PREMIUM', current_kdn = 0.12, is_restructuring_active = false;
""")

    # 2. UPSERT В CLIENT_PROFILES
    sql_statements.append("""
-- 2. client_profiles
INSERT INTO client_profiles (
    client_token, iin, full_name, age, gender, city, employment_type, industry,
    declared_income, archetype, stress_narrative, is_under_stalker_watch,
    current_risk_score, risk_level, created_at, updated_at
)
VALUES (
    '11111111-2222-3333-4444-555555555555',
    '970415301824',
    'Арман Сейткалиев',
    29,
    'MALE',
    'Алматы',
    'OFFICIAL_EMPLOYED',
    'IT',
    1200000.0,
    'TECH_OPTIMIST',
    'Lead Backend Architect в ТОО QazFinTech Solutions (Astana Hub). Эталонный профиль Класса AAA, DTI 12.08%, скоринг ПКБ 0.88, 0 дней просрочки.',
    true,
    0.0105,
    'GREEN',
    '2023-10-15 00:00:00+00',
    NOW()
)
ON CONFLICT (client_token) DO UPDATE
SET full_name = 'Арман Сейткалиев',
    iin = '970415301824',
    declared_income = 1200000.0,
    current_risk_score = 0.0105,
    risk_level = 'GREEN',
    is_under_stalker_watch = true,
    updated_at = NOW();
""")

    # 3. UPSERT В LOANS
    sql_statements.append("""
-- 3. loans
INSERT INTO loans (
    loan_id, client_token, account_number, original_principal, current_principal_balance,
    interest_rate, effective_rate_gesv, monthly_payment, maturity_date,
    days_past_due, stage_ifrs9, status, updated_at
)
VALUES (
    '511cade2-8439-4a51-a781-4422cdd1e7b6',
    '11111111-2222-3333-4444-555555555555',
    'KZ886010002003004001',
    4200000.00,
    4200000.00,
    0.175,
    0.175,
    145000.00,
    '2026-10-15',
    0,
    'STAGE_1',
    'ACTIVE',
    NOW()
)
ON CONFLICT (loan_id) DO UPDATE
SET current_principal_balance = 4200000.00,
    monthly_payment = 145000.00,
    days_past_due = 0,
    stage_ifrs9 = 'STAGE_1',
    status = 'ACTIVE',
    updated_at = NOW();

-- Также для совместимости с 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
INSERT INTO loans (
    loan_id, client_token, account_number, original_principal, current_principal_balance,
    interest_rate, effective_rate_gesv, monthly_payment, maturity_date,
    days_past_due, stage_ifrs9, status, updated_at
)
VALUES (
    'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
    '11111111-2222-3333-4444-555555555555',
    'KZ886010002003004001',
    4200000.00,
    4200000.00,
    0.175,
    0.175,
    145000.00,
    '2026-10-15',
    0,
    'STAGE_1',
    'ACTIVE',
    NOW()
)
ON CONFLICT (loan_id) DO UPDATE
SET current_principal_balance = 4200000.00,
    monthly_payment = 145000.00,
    days_past_due = 0,
    stage_ifrs9 = 'STAGE_1',
    status = 'ACTIVE',
    updated_at = NOW();
""")

    # 4. UPSERT В SCORING_EVENTS
    feature_snapshot = {
        "AMT_INCOME_TOTAL": 1200000.0,
        "AMT_CREDIT": 4200000.0,
        "AMT_ANNUITY": 145000.0,
        "dti_ratio": 0.1208,
        "EXT_SOURCE_2": 0.88,
        "inst_avg_delay_days": -5.4,
        "inst_late_count": 0,
        "pos_completed_count": 2,
        "cc_atm_drawings_sum": 0.0,
        "cc_pos_drawings_sum": 320000.0,
        "cc_utilization_mean": 0.18,
    }
    shap_factors = [
        {"feature": "DTI_RATIO", "value": "12.08%", "impact": -0.42, "description": "Минимальная долговая нагрузка"},
        {"feature": "EXT_SOURCE_2", "value": "0.88", "impact": -0.38, "description": "Высший кредитный рейтинг ПКБ"},
        {"feature": "INST_AVG_DELAY", "value": "-5.40 дн.", "impact": -0.29, "description": "Опережение графика платежей"},
        {"feature": "POS_COMPLETED", "value": "2 договора", "impact": -0.15, "description": "Успешно закрытые BNPL рассрочки"},
        {"feature": "CC_ATM_SUM", "value": "0 ₸", "impact": -0.12, "description": "Отсутствие снятия наличных в банкоматах"},
    ]

    sql_statements.append(f"""
-- 4. scoring_events
INSERT INTO scoring_events (
    event_id, loan_id, p_default_30d, p_default_60d, model_version, shap_factors, feature_snapshot, triggered_at
)
VALUES (
    'aaaaaaaa-bbbb-cccc-dddd-111111111111',
    '511cade2-8439-4a51-a781-4422cdd1e7b6',
    0.0105,
    0.0125,
    'Full360CrossAttentionNet_v1.0',
    '{json.dumps(shap_factors, ensure_ascii=False)}'::jsonb,
    '{json.dumps(feature_snapshot, ensure_ascii=False)}'::jsonb,
    NOW()
)
ON CONFLICT (event_id) DO UPDATE
SET p_default_30d = 0.0105, p_default_60d = 0.0125, triggered_at = NOW();
""")

    # 5. СОЗДАНИЕ СПЕЦИАЛЬНЫХ ТАБЛИЦ ДЛЯ 360° ДАННЫХ АРМАНА
    sql_statements.append("""
-- 5. Специализированные таблицы истории 360°
CREATE TABLE IF NOT EXISTS arman_installments_payments (
    id SERIAL PRIMARY KEY,
    sk_id_prev BIGINT,
    num_instalment_number INT,
    days_instalment DOUBLE PRECISION,
    days_entry_payment DOUBLE PRECISION,
    amt_instalment NUMERIC(14,2),
    amt_payment NUMERIC(14,2),
    delay_days DOUBLE PRECISION,
    scheduled_pay_date DATE,
    actual_pay_date DATE,
    days_early DOUBLE PRECISION,
    payment_status VARCHAR(50),
    receipt_id VARCHAR(50),
    payment_channel VARCHAR(100),
    salary_linked VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS arman_pos_cash_balance (
    id SERIAL PRIMARY KEY,
    sk_id_prev BIGINT,
    months_balance INT,
    cnt_instalment INT,
    cnt_instalment_future INT,
    name_contract_status VARCHAR(50),
    sk_dpd INT,
    contract_number VARCHAR(100),
    store_name VARCHAR(150),
    product_description VARCHAR(255),
    monthly_installment_kzt NUMERIC(14,2)
);

CREATE TABLE IF NOT EXISTS arman_credit_card_balance (
    id SERIAL PRIMARY KEY,
    statement_month VARCHAR(20),
    months_balance INT,
    amt_balance NUMERIC(14,2),
    amt_credit_limit_actual NUMERIC(14,2),
    amt_drawings_atm_current NUMERIC(14,2),
    amt_drawings_pos_current NUMERIC(14,2),
    amt_payment_total_current NUMERIC(14,2),
    cashback_earned_kzt NUMERIC(14,2),
    grace_period_status VARCHAR(100),
    card_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS arman_bank_statement_transactions (
    tx_id VARCHAR(50) PRIMARY KEY,
    date_time TIMESTAMP,
    category VARCHAR(50),
    mcc INT,
    merchant VARCHAR(150),
    amount NUMERIC(14,2),
    direction VARCHAR(20),
    balance_after NUMERIC(14,2),
    city VARCHAR(50),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS arman_telemetry_stream (
    event_id VARCHAR(50) PRIMARY KEY,
    timestamp TIMESTAMP,
    event_type VARCHAR(50),
    auth_method VARCHAR(100),
    ip_address VARCHAR(50),
    geo_location VARCHAR(100),
    screen_view VARCHAR(100),
    session_duration_sec INT,
    risk_signal VARCHAR(50),
    description TEXT
);
""")

    # 6. ОЧИСТКА И ЗАПОЛНЕНИЕ ДАННЫХ
    sql_statements.append("TRUNCATE TABLE arman_installments_payments;")
    for _, row in df_inst.iterrows():
        sql_statements.append(f"""
INSERT INTO arman_installments_payments (
    sk_id_prev, num_instalment_number, days_instalment, days_entry_payment,
    amt_instalment, amt_payment, delay_days, scheduled_pay_date, actual_pay_date,
    days_early, payment_status, receipt_id, payment_channel, salary_linked
) VALUES (
    {row['SK_ID_PREV']}, {row['NUM_INSTALMENT_NUMBER']}, {row['DAYS_INSTALMENT']}, {row['DAYS_ENTRY_PAYMENT']},
    {row['AMT_INSTALMENT']}, {row['AMT_PAYMENT']}, {row['DELAY_DAYS']}, '{row['SCHEDULED_PAY_DATE']}', '{row['ACTUAL_PAY_DATE']}',
    {row['DAYS_EARLY']}, '{row['PAYMENT_STATUS']}', '{row['RECEIPT_ID']}', '{row['PAYMENT_CHANNEL']}', '{row['SALARY_LINKED']}'
);""")

    sql_statements.append("TRUNCATE TABLE arman_pos_cash_balance;")
    for _, row in df_pos.iterrows():
        sql_statements.append(f"""
INSERT INTO arman_pos_cash_balance (
    sk_id_prev, months_balance, cnt_instalment, cnt_instalment_future, name_contract_status,
    sk_dpd, contract_number, store_name, product_description, monthly_installment_kzt
) VALUES (
    {row['SK_ID_PREV']}, {row['MONTHS_BALANCE']}, {row['CNT_INSTALMENT']}, {row['CNT_INSTALMENT_FUTURE']}, '{row['NAME_CONTRACT_STATUS']}',
    {row['SK_DPD']}, '{row['CONTRACT_NUMBER']}', '{row['STORE_NAME']}', '{row['PRODUCT_DESCRIPTION']}', {row['MONTHLY_INSTALLMENT_KZT']}
);""")

    sql_statements.append("TRUNCATE TABLE arman_credit_card_balance;")
    for _, row in df_cc.iterrows():
        sql_statements.append(f"""
INSERT INTO arman_credit_card_balance (
    statement_month, months_balance, amt_balance, amt_credit_limit_actual,
    amt_drawings_atm_current, amt_drawings_pos_current, amt_payment_total_current,
    cashback_earned_kzt, grace_period_status, card_type
) VALUES (
    '{row['STATEMENT_MONTH']}', {row['MONTHS_BALANCE']}, {row['AMT_BALANCE']}, {row['AMT_CREDIT_LIMIT_ACTUAL']},
    {row['AMT_DRAWINGS_ATM_CURRENT']}, {row['AMT_DRAWINGS_POS_CURRENT']}, {row['AMT_PAYMENT_TOTAL_CURRENT']},
    {row['CASHBACK_EARNED_KZT']}, '{row['GRACE_PERIOD_STATUS']}', '{row['CARD_TYPE']}'
);""")

    sql_statements.append("TRUNCATE TABLE arman_bank_statement_transactions;")
    for _, row in df_tx.iterrows():
        notes_esc = str(row['NOTES']).replace("'", "''")
        merchant_esc = str(row['MERCHANT']).replace("'", "''")
        sql_statements.append(f"""
INSERT INTO arman_bank_statement_transactions (
    tx_id, date_time, category, mcc, merchant, amount, direction, balance_after, city, notes
) VALUES (
    '{row['TX_ID']}', '{row['DATE_TIME']}', '{row['CATEGORY']}', {row['MCC']}, '{merchant_esc}',
    {row['AMOUNT']}, '{row['DIRECTION']}', {row['BALANCE_AFTER']}, '{row['CITY']}', '{notes_esc}'
);""")

    sql_statements.append("TRUNCATE TABLE arman_telemetry_stream;")
    for _, row in df_telem.iterrows():
        desc_esc = str(row['DESCRIPTION']).replace("'", "''")
        sql_statements.append(f"""
INSERT INTO arman_telemetry_stream (
    event_id, timestamp, event_type, auth_method, ip_address, geo_location,
    screen_view, session_duration_sec, risk_signal, description
) VALUES (
    '{row['EVENT_ID']}', '{row['TIMESTAMP']}', '{row['EVENT_TYPE']}', '{row['AUTH_METHOD']}',
    '{row['IP_ADDRESS']}', '{row['GEO_LOCATION']}', '{row['SCREEN_VIEW']}', {row['SESSION_DURATION_SEC']},
    '{row['RISK_SIGNAL']}', '{desc_esc}'
);""")

    # 7. ДОБАВЛЕНИЕ СНАПШОТОВ В STALKER_TIMELINE_SNAPSHOTS
    sql_statements.append("""
-- 7. stalker_timeline_snapshots
DELETE FROM stalker_timeline_snapshots WHERE client_token = '11111111-2222-3333-4444-555555555555';

INSERT INTO stalker_timeline_snapshots (
    snapshot_id, client_token, timestamp, risk_score, delta_pd, salary_trend, salary_delay_days,
    has_mfo_activity, active_bnpl_count, dti_estimate, daily_balance_7d, dbo_checks_count, primary_trigger
)
VALUES
(gen_random_uuid(), '11111111-2222-3333-4444-555555555555', NOW() - INTERVAL '60 days', 0.012, -0.002, 1.0, 0, false, 0, 0.1208, 650000, 1, 'SALARY_PAYROLL_INFLOW'),
(gen_random_uuid(), '11111111-2222-3333-4444-555555555555', NOW() - INTERVAL '35 days', 0.011, -0.001, 1.35, 0, false, 0, 0.092, 980000, 1, 'QUARTERLY_RELEASE_BONUS'),
(gen_random_uuid(), '11111111-2222-3333-4444-555555555555', NOW() - INTERVAL '20 days', 0.010, -0.001, 1.0, 0, false, 0, 0.1208, 620000, 1, 'INSTALLMENT_EARLY_PAY'),
(gen_random_uuid(), '11111111-2222-3333-4444-555555555555', NOW() - INTERVAL '7 days', 0.011, 0.001, 1.0, 0, false, 0, 0.1208, 590000, 3, 'DBO_NIGHT_SESSION_INSPECT'),
(gen_random_uuid(), '11111111-2222-3333-4444-555555555555', NOW(), 0.0105, -0.0005, 1.0, 0, false, 0, 0.1208, 650000, 1, 'BASE_AFFLUENT_HEALTHY');
""")

    # Запись в файл
    full_sql = "\n".join(sql_statements)
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write(full_sql)

    print(f"📝 SQL-скрипт сгенерирован: {sql_file} ({len(full_sql):,} байт)")

    # Выполнение через docker exec
    print("\n🚀 Выполнение миграции в PostgreSQL через контейнер risktwin-postgres...")
    cmd = ["docker", "exec", "-i", "risktwin-postgres", "psql", "-U", "risktwin_user", "-d", "risktwin_db"]
    res = subprocess.run(cmd, input=full_sql.encode("utf-8"), capture_output=True)

    if res.returncode == 0:
        print("✅ Миграция успешно завершена в PostgreSQL!")
    else:
        print(f"❌ Ошибка миграции: {res.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    migrate_to_postgres()
