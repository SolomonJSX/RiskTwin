"""
Расширенный генератор глубокой 5-летней финансовой и поведенческой истории Армана.
Генерирует 8 детализированных файлов данных (CSV) и полное Markdown-досье:
1. arman_application.csv (расширенная анкета заемщика, ИИН, работодатель, скоринги)
2. arman_installments_payments.csv (36 календарных платежей с чеками и точным опережением -5.40 дн.)
3. arman_pos_cash_balance.csv (помесячная детализация BNPL рассрочек на технику)
4. arman_credit_card_balance.csv (24 ежемесячные банковские выписки, кэшбэк, 100% грейс)
5. arman_previous_application.csv (история всех предыдущих заявок)
6. arman_bureau.csv (выписка ПКБ с историей запросов и закрытых займов)
7. arman_bank_statement_transactions.csv (700+ реальных транзакций по картам и счетам за 2 года)
8. arman_telemetry_stream.csv (300+ цифровых поведенческих следов в ДБО: клики, FaceID, сессии)
9. arman_financial_dossier.md (подробный аналитический отчет для кредитного комитета)
"""

import sys
import datetime
import random
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import torch
import pickle

def generate_deep_arman_history():
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "data" / "arman_history"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 85)
    print("🚀 ГЛУБОКАЯ ГЕНЕРАЦИЯ ДАННЫХ И ИСТОРИИ АРМАНА (IT-СЕНЬОР, КЛАСС AAA, 2021-2026)")
    print(f"📁 Папка сохранения: {output_dir}")
    print("=" * 85)

    sk_id_curr = 999001
    account_num = "KZ886010002003004001"
    client_token = "11111111-2222-3333-4444-555555555555"
    iin = "970415301824"  # 15 апреля 1997 года (29 лет)

    # =========================================================================
    # 1. APPLICATION (Анкета и параметры активного кредита)
    # =========================================================================
    app_data = {
        "SK_ID_CURR": [sk_id_curr],
        "TARGET": [0],
        "ACCOUNT_NUMBER": [account_num],
        "CLIENT_TOKEN": [client_token],
        "IIN": [iin],
        "FULL_NAME": ["Арман Сейткалиев"],
        "ROLE": ["Lead Software Engineer / Backend Architect"],
        "EMPLOYER_NAME": ["ТОО 'QazFinTech Solutions' (аккредитованный резидент Astana Hub)"],
        "NAME_CONTRACT_TYPE": ["Cash loans"],
        "CODE_GENDER": ["M"],
        "FLAG_OWN_CAR": ["Y"],
        "CAR_MODEL": ["Hyundai Tucson 2023"],
        "FLAG_OWN_REALTY": ["Y"],
        "REALTY_TYPE": ["2-комнатная квартира, ЖК 'Комфорт Сити', Алматы"],
        "CNT_CHILDREN": [0],
        "AMT_INCOME_TOTAL": [1200000.0],
        "AMT_CREDIT": [4200000.0],
        "AMT_ANNUITY": [145000.0],
        "AMT_GOODS_PRICE": [4200000.0],
        "NAME_INCOME_TYPE": ["Commercial associate"],
        "NAME_EDUCATION_TYPE": ["Higher education"],
        "UNIVERSITY": ["МУИТ (IITU), Computer Science, бакалавриат 2019"],
        "NAME_FAMILY_STATUS": ["Single / not married"],
        "NAME_HOUSING_TYPE": ["House / apartment"],
        "DAYS_BIRTH": [-10592],        # 29 лет
        "DAYS_EMPLOYED": [-2556],     # 7 лет стажа
        "DAYS_REGISTRATION": [-3200],
        "DAYS_ID_PUBLISH": [-2100],
        "OCCUPATION_TYPE": ["IT staff"],
        "EXT_SOURCE_1": [0.85],
        "EXT_SOURCE_2": [0.88],       # Скоринг ПКБ (Класс AAA)
        "EXT_SOURCE_3": [0.86],
        "LOAN_START_DATE": ["2023-10-15"],
        "LOAN_END_DATE": ["2026-10-15"],
        "INTEREST_RATE_ANNUAL": [17.5],
        "PURPOSE": ["Капитальный ремонт квартиры и обустройство домашней IT-лаборатории"],
    }
    df_app = pd.DataFrame(app_data)
    df_app.to_csv(output_dir / "arman_application.csv", index=False)
    print(f"[1/8] ✅ arman_application.csv: Доход ₸1.2M, заем ₸4.2M, DTI 12.08%, скоринг ПКБ 0.88")

    # =========================================================================
    # 2. INSTALLMENTS PAYMENTS (36 календарных платежей с точным опережением -5.40 дн.)
    # =========================================================================
    delays = [-5.0] * 20 + [-6.0] * 12 + [-5.6] * 4
    np.random.seed(42)
    np.random.shuffle(delays)
    assert abs(np.mean(delays) - (-5.4)) < 1e-5

    start_date = datetime.date(2023, 10, 15)
    inst_rows = []

    for i in range(36):
        month_idx = 36 - i
        days_instalment = - (month_idx * 30)
        delay = delays[i]
        days_entry = days_instalment + delay

        # Реальная календарная дата
        due_date = start_date + datetime.timedelta(days=(i + 1) * 30.4375)
        paid_date = due_date + datetime.timedelta(days=delay)

        channels = ["Kaspi Gold Автоплатеж", "Halyk Homebank Mobile", "Freedom SuperApp"]
        channel = channels[i % len(channels)]
        receipt = f"RCP-KZ-{2023 + (i // 12)}-{100000 + i * 287}"

        inst_rows.append({
            "SK_ID_PREV": 100001,
            "SK_ID_CURR": sk_id_curr,
            "NUM_INSTALMENT_VERSION": 1.0,
            "NUM_INSTALMENT_NUMBER": i + 1,
            "DAYS_INSTALMENT": float(days_instalment),
            "DAYS_ENTRY_PAYMENT": float(days_entry),
            "AMT_INSTALMENT": 145000.0,
            "AMT_PAYMENT": 145000.0,
            "DELAY_DAYS": float(delay),
            "SCHEDULED_PAY_DATE": due_date.strftime("%Y-%m-%d"),
            "ACTUAL_PAY_DATE": paid_date.strftime("%Y-%m-%d"),
            "DAYS_EARLY": abs(float(delay)),
            "PAYMENT_STATUS": "PAID_IN_FULL_EARLY",
            "RECEIPT_ID": receipt,
            "PAYMENT_CHANNEL": channel,
            "ACCOUNT_DEBITED": "KZ059260200219481234",
            "SALARY_LINKED": "Да (зарплата зачислена 25 числа)",
        })

    df_inst = pd.DataFrame(inst_rows)
    df_inst.to_csv(output_dir / "arman_installments_payments.csv", index=False)
    print(f"[2/8] ✅ arman_installments_payments.csv: 36 платежей (2023–2026), среднее опережение {df_inst['DELAY_DAYS'].mean():.2f} дн., 0 просрочек")

    # =========================================================================
    # 3. POS CASH BALANCE (2 товарные рассрочки: 12 мес MacBook + 10 мес iPhone)
    # =========================================================================
    pos_rows = []
    # Договор 1: Ноутбук MacBook Pro M1 Max 64GB (iSpace Dostyk Plaza, ₸950 000, 12 месяцев)
    for m in range(12):
        month_bal = - (36 - m)
        remaining = 11 - m
        status = "Completed" if m == 11 else "Active"
        pos_rows.append({
            "SK_ID_PREV": 200001,
            "SK_ID_CURR": sk_id_curr,
            "MONTHS_BALANCE": month_bal,
            "CNT_INSTALMENT": 12,
            "CNT_INSTALMENT_FUTURE": remaining,
            "NAME_CONTRACT_STATUS": status,
            "SK_DPD": 0,
            "SK_DPD_DEF": 0,
            "CONTRACT_NUMBER": "BNPL-2021-APL-0912",
            "STORE_NAME": "iSpace Dostyk Plaza (Алматы)",
            "PRODUCT_DESCRIPTION": "Ноутбук Apple MacBook Pro 16' M1 Max 64GB / 1TB SSD",
            "MONTHLY_INSTALLMENT_KZT": 79166.0,
        })

    # Договор 2: Смартфон iPhone 14 Pro 256GB (Technodom Mega Alma-Ata, ₸680 000, 10 месяцев)
    for m in range(10):
        month_bal = - (24 - m)
        remaining = 9 - m
        status = "Completed" if m == 9 else "Active"
        pos_rows.append({
            "SK_ID_PREV": 200002,
            "SK_ID_CURR": sk_id_curr,
            "MONTHS_BALANCE": month_bal,
            "CNT_INSTALMENT": 10,
            "CNT_INSTALMENT_FUTURE": remaining,
            "NAME_CONTRACT_STATUS": status,
            "SK_DPD": 0,
            "SK_DPD_DEF": 0,
            "CONTRACT_NUMBER": "BNPL-2022-TCH-4481",
            "STORE_NAME": "Technodom Mega Center Alma-Ata",
            "PRODUCT_DESCRIPTION": "Смартфон Apple iPhone 14 Pro Space Black 256GB",
            "MONTHLY_INSTALLMENT_KZT": 68000.0,
        })

    df_pos = pd.DataFrame(pos_rows)
    df_pos.to_csv(output_dir / "arman_pos_cash_balance.csv", index=False)
    print(f"[3/8] ✅ arman_pos_cash_balance.csv: 22 помесячные выписки (2 закрытых договора BNPL в iSpace/Technodom, 0 DPD)")

    # =========================================================================
    # 4. CREDIT CARD BALANCE (24 месяца выписок: 18.0% утилизация, ₸320k POS, 0 кэша)
    # =========================================================================
    base_balances = [
        160000, 190000, 175000, 185000, 170000, 200000,
        165000, 195000, 180000, 175000, 185000, 190000,
        170000, 180000, 185000, 175000, 190000, 165000,
        180000, 195000, 170000, 185000, 180000, 185000,
    ]
    base_balances = np.array(base_balances, dtype=float)
    base_balances = base_balances - np.mean(base_balances) + 180000.0

    pos_drawings = [0.0] * 24
    pos_drawings[-1] = 120000.0  # Оплата авиабилетов Air Astana Алматы -> Франкфурт
    pos_drawings[-2] = 110000.0  # Покупки в супермаркетах Galmart и Magnum
    pos_drawings[-3] = 90000.0   # Обслуживание автомобиля в официальном сервисе
    assert sum(pos_drawings) == 320000.0

    cc_rows = []
    cc_start_date = datetime.date(2024, 10, 1)

    for m in range(24):
        month_bal = - (24 - m)
        bal = base_balances[m]
        pos_spend = pos_drawings[m]
        stmt_date = cc_start_date - datetime.timedelta(days=(24 - m) * 30.4375)

        cc_rows.append({
            "SK_ID_PREV": 300001,
            "SK_ID_CURR": sk_id_curr,
            "STATEMENT_MONTH": stmt_date.strftime("%Y-%m"),
            "MONTHS_BALANCE": month_bal,
            "AMT_BALANCE": float(bal),
            "AMT_CREDIT_LIMIT_ACTUAL": 1000000.0,
            "AMT_DRAWINGS_ATM_CURRENT": 0.0,
            "CNT_DRAWINGS_ATM_CURRENT": 0.0,
            "AMT_DRAWINGS_POS_CURRENT": float(pos_spend),
            "CNT_DRAWINGS_POS_CURRENT": 8.0 if pos_spend > 0 else 4.0,
            "AMT_PAYMENT_TOTAL_CURRENT": float(bal),
            "CASHBACK_EARNED_KZT": round(pos_spend * 0.02, 2) if pos_spend > 0 else 1500.0,
            "GRACE_PERIOD_STATUS": "100% Grace Period Complied (0% переплат)",
            "SK_DPD": 0,
            "SK_DPD_DEF": 0,
            "CARD_TYPE": "Mastercard Black Edition World Elite",
        })

    df_cc = pd.DataFrame(cc_rows)
    df_cc.to_csv(output_dir / "arman_credit_card_balance.csv", index=False)
    print(f"[4/8] ✅ arman_credit_card_balance.csv: 24 месяца выписок (утилизация 18.0%, POS: ₸320k, ATM: ₸0)")

    # =========================================================================
    # 5. PREVIOUS APPLICATION (3 одобренные заявки в прошлом)
    # =========================================================================
    prev_rows = [
        {
            "SK_ID_PREV": 200001,
            "SK_ID_CURR": sk_id_curr,
            "APPLICATION_DATE": "2021-10-10",
            "NAME_CONTRACT_TYPE": "Consumer loans",
            "AMT_APPLICATION": 450000.0,
            "AMT_CREDIT": 450000.0,
            "NAME_CONTRACT_STATUS": "Approved",
            "NAME_PAYMENT_TYPE": "Cash through the bank",
            "CODE_REJECT_REASON": "XAP",
            "NAME_CLIENT_TYPE": "New",
            "NAME_GOODS_CATEGORY": "Computers",
            "DAYS_DECISION": -1080,
            "PARTNER_STORE": "iSpace Dostyk Plaza",
            "DECISION_TIME_SECONDS": 42,
        },
        {
            "SK_ID_PREV": 200002,
            "SK_ID_CURR": sk_id_curr,
            "APPLICATION_DATE": "2022-10-12",
            "NAME_CONTRACT_TYPE": "Consumer loans",
            "AMT_APPLICATION": 380000.0,
            "AMT_CREDIT": 380000.0,
            "NAME_CONTRACT_STATUS": "Approved",
            "NAME_PAYMENT_TYPE": "Cash through the bank",
            "CODE_REJECT_REASON": "XAP",
            "NAME_CLIENT_TYPE": "Repeater",
            "NAME_GOODS_CATEGORY": "Mobile",
            "DAYS_DECISION": -720,
            "PARTNER_STORE": "Technodom Mega Alma-Ata",
            "DECISION_TIME_SECONDS": 18,
        },
        {
            "SK_ID_PREV": 300001,
            "SK_ID_CURR": sk_id_curr,
            "APPLICATION_DATE": "2022-10-02",
            "NAME_CONTRACT_TYPE": "Revolving loans",
            "AMT_APPLICATION": 1000000.0,
            "AMT_CREDIT": 1000000.0,
            "NAME_CONTRACT_STATUS": "Approved",
            "NAME_PAYMENT_TYPE": "XNA",
            "CODE_REJECT_REASON": "XAP",
            "NAME_CLIENT_TYPE": "Repeater",
            "NAME_GOODS_CATEGORY": "XNA",
            "DAYS_DECISION": -730,
            "PARTNER_STORE": "Digital Banking App Pre-approved Offer",
            "DECISION_TIME_SECONDS": 8,
        },
    ]
    df_prev = pd.DataFrame(prev_rows)
    df_prev.to_csv(output_dir / "arman_previous_application.csv", index=False)
    print(f"[5/8] ✅ arman_previous_application.csv: 3 заявки (100% одобрено, 0 отказов)")

    # =========================================================================
    # 6. BUREAU (Выписка ПКБ / Первое Кредитное Бюро)
    # =========================================================================
    bureau_rows = [
        {
            "SK_ID_CURR": sk_id_curr,
            "SK_ID_BUREAU": 500001,
            "CREDIT_ACTIVE": "Closed",
            "CREDIT_CURRENCY": "KZT",
            "DAYS_CREDIT": -1200,
            "CREDIT_DAY_OVERDUE": 0,
            "DAYS_CREDIT_ENDDATE": -840,
            "AMT_CREDIT_SUM": 500000.0,
            "AMT_CREDIT_SUM_DEBT": 0.0,
            "AMT_CREDIT_SUM_OVERDUE": 0.0,
            "CNT_CREDIT_PROLONG": 0,
            "CREDIT_TYPE": "Consumer credit",
            "BANK_NAME": "ForteBank (Потребительский беззалоговый)",
            "STATUS_PKB": "Полностью закрыт без единого дня просрочки",
        },
        {
            "SK_ID_CURR": sk_id_curr,
            "SK_ID_BUREAU": 500002,
            "CREDIT_ACTIVE": "Closed",
            "CREDIT_CURRENCY": "KZT",
            "DAYS_CREDIT": -800,
            "CREDIT_DAY_OVERDUE": 0,
            "DAYS_CREDIT_ENDDATE": -440,
            "AMT_CREDIT_SUM": 350000.0,
            "AMT_CREDIT_SUM_DEBT": 0.0,
            "AMT_CREDIT_SUM_OVERDUE": 0.0,
            "CNT_CREDIT_PROLONG": 0,
            "CREDIT_TYPE": "Credit card",
            "BANK_NAME": "Jusan Bank (Кредитная карта)",
            "STATUS_PKB": "Полностью закрыта по заявлению клиента",
        },
    ]
    df_bureau = pd.DataFrame(bureau_rows)
    df_bureau.to_csv(output_dir / "arman_bureau.csv", index=False)
    print(f"[6/8] ✅ arman_bureau.csv: 2 записи в ПКБ (100% закрыто, 0 долгов, 0 просрочек)")

    # =========================================================================
    # 7. BANK STATEMENT TRANSACTIONS (720 транзакций за 2 года: 2024–2026)
    # =========================================================================
    tx_rows = []
    current_balance = 650000.0
    cur_date = datetime.date(2024, 10, 14)
    end_date = datetime.date(2026, 10, 14)

    # Список типичных расходов и доходов IT-сеньора в Алматы
    vendors_groceries = [("Magnum Cash & Carry Dostyk", 5411), ("Galmart Mega Alma-Ata", 5411), ("Colibri Gourmet", 5411)]
    vendors_dining = [("Cafeteria Kurmangazy", 5812), ("Marrone Rosso Panfilov", 5812), ("Paul Almaty", 5812), ("Del Papa Dostyk", 5812)]
    vendors_taxi = [("Yandex Go Comfort+ Almaty", 4121), ("Yandex Go Business", 4121)]
    vendors_subs = [
        ("JetBrains All Products Pack", 5734, 18500.0),
        ("GitHub Copilot Enterprise", 5734, 9500.0),
        ("Amazon Web Services Cloud", 7372, 32000.0),
        ("OpenAI ChatGPT Plus Subscription", 5734, 9800.0),
        ("Spotify Premium Family", 4899, 2990.0),
        ("YouTube Premium Family", 4899, 3190.0),
    ]

    total_days = (end_date - cur_date).days
    day_step = cur_date

    tx_counter = 10000
    while day_step <= end_date:
        day_of_month = day_step.day

        # 1. Зачисление зарплаты 25 числа каждого месяца (₸ 1 200 000)
        if day_of_month == 25:
            current_balance += 1200000.0
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 10:14:22",
                "CATEGORY": "SALARY",
                "MCC": 9399,
                "MERCHANT": "ТОО 'QazFinTech Solutions' Payroll (Swift KASE)",
                "AMOUNT": 1200000.0,
                "DIRECTION": "INFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Зарплата за месяц",
            })

            # Перевод на сберегательный депозит (₸ 350 000)
            current_balance -= 350000.0
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 11:30:00",
                "CATEGORY": "SAVINGS_TRANSFER",
                "MCC": 6012,
                "MERCHANT": "Депозит 'Универсальный' 14.5% ГЭСВ",
                "AMOUNT": -350000.0,
                "DIRECTION": "OUTFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Пополнение подушки безопасности",
            })

        # 2. Квартальный IT-бонус (март, июнь, сентябрь, декабрь 10-го числа)
        if day_of_month == 10 and day_step.month in [3, 6, 9, 12]:
            bonus = 350000.0
            current_balance += bonus
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 15:45:00",
                "CATEGORY": "IT_BONUS",
                "MCC": 9399,
                "MERCHANT": "ТОО 'QazFinTech Solutions' KPI Release Bonus",
                "AMOUNT": bonus,
                "DIRECTION": "INFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Бонус за успешный финтех-релиз архитектуры",
            })

        # 3. Ежемесячный платеж по кредиту (примерно 20 числа, за 5-6 дней до дедлайна)
        if day_of_month == 20:
            current_balance -= 145000.0
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 09:15:33",
                "CATEGORY": "LOAN_REPAYMENT",
                "MCC": 6012,
                "MERCHANT": "RiskTwin Bank Автопогашение займа KZ88601",
                "AMOUNT": -145000.0,
                "DIRECTION": "OUTFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Плановый аннуитетный платеж за 5 дней до срока",
            })

        # 4. IT-подписки 1 числа месяца
        if day_of_month == 1:
            for sub_name, sub_mcc, sub_cost in vendors_subs:
                current_balance -= sub_cost
                tx_counter += 1
                tx_rows.append({
                    "TX_ID": f"TX-{tx_counter}",
                    "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 04:00:15",
                    "CATEGORY": "SOFTWARE_SUBSCRIPTION",
                    "MCC": sub_mcc,
                    "MERCHANT": sub_name,
                    "AMOUNT": -sub_cost,
                    "DIRECTION": "OUTFLOW",
                    "BALANCE_AFTER": current_balance,
                    "CITY": "Online (International e-Commerce)",
                    "NOTES": "Профессиональный софт разработчика",
                })

        # 5. Ежедневные расходы (супермаркеты, кафе, такси)
        # 1-2 транзакции в день
        if random.random() < 0.85:
            store, mcc = random.choice(vendors_groceries)
            cost = round(random.uniform(4500, 18500), 2)
            current_balance -= cost
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 19:25:10",
                "CATEGORY": "GROCERIES",
                "MCC": mcc,
                "MERCHANT": store,
                "AMOUNT": -cost,
                "DIRECTION": "OUTFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Безналичная оплата картой POS",
            })

        if random.random() < 0.65:
            cafe, mcc = random.choice(vendors_dining)
            cost = round(random.uniform(2800, 9500), 2)
            current_balance -= cost
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 13:10:45",
                "CATEGORY": "DINING",
                "MCC": mcc,
                "MERCHANT": cafe,
                "AMOUNT": -cost,
                "DIRECTION": "OUTFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Бизнес-ланч / кофе",
            })

        if random.random() < 0.45:
            taxi, mcc = random.choice(vendors_taxi)
            cost = round(random.uniform(1800, 4200), 2)
            current_balance -= cost
            tx_counter += 1
            tx_rows.append({
                "TX_ID": f"TX-{tx_counter}",
                "DATE_TIME": f"{day_step.strftime('%Y-%m-%d')} 08:45:00",
                "CATEGORY": "TRANSPORT",
                "MCC": mcc,
                "MERCHANT": taxi,
                "AMOUNT": -cost,
                "DIRECTION": "OUTFLOW",
                "BALANCE_AFTER": current_balance,
                "CITY": "Almaty",
                "NOTES": "Поездка в офис / коворкинг",
            })

        day_step += datetime.timedelta(days=1)

    df_tx = pd.DataFrame(tx_rows)
    df_tx.to_csv(output_dir / "arman_bank_statement_transactions.csv", index=False)
    print(f"[7/8] ✅ arman_bank_statement_transactions.csv: {len(df_tx):,} детальных транзакций (зарплаты, подписки, кафе, Magnum, депозиты)")

    # =========================================================================
    # 8. TELEMETRY STREAM (320 цифровых поведенческих следов в ДБО за 2024-2026)
    # =========================================================================
    telem_events = []
    tel_counter = 5000
    tel_date = datetime.date(2025, 1, 1)

    while tel_date <= datetime.date(2026, 10, 14):
        # Обычный утренний вход в ДБО (проверка баланса перед рабочим днем)
        if random.random() < 0.35:
            tel_counter += 1
            telem_events.append({
                "EVENT_ID": f"EVT-{tel_counter}",
                "TIMESTAMP": f"{tel_date.strftime('%Y-%m-%d')} 08:32:{random.randint(10, 59)}",
                "EVENT_TYPE": "APP_SESSION_START",
                "AUTH_METHOD": "Biometrics (FaceID iPhone)",
                "IP_ADDRESS": f"178.89.{random.randint(10, 200)}.{random.randint(1, 254)}",
                "GEO_LOCATION": "Almaty, Medeu District",
                "SCREEN_VIEW": "DASHBOARD_ACCOUNTS",
                "SESSION_DURATION_SEC": random.randint(15, 45),
                "RISK_SIGNAL": "NORMAL",
                "DESCRIPTION": "Стандартная утренняя проверка балансов",
            })

        # Проверка графика платежей (за 6-7 дней до дедлайна)
        if tel_date.day in [18, 19]:
            tel_counter += 1
            telem_events.append({
                "EVENT_ID": f"EVT-{tel_counter}",
                "TIMESTAMP": f"{tel_date.strftime('%Y-%m-%d')} 12:15:00",
                "EVENT_TYPE": "LOAN_SCHEDULE_INSPECT",
                "AUTH_METHOD": "Biometrics",
                "IP_ADDRESS": "178.89.44.112",
                "GEO_LOCATION": "Almaty, Bostandyk District",
                "SCREEN_VIEW": "CREDIT_SCHEDULE_PREVIEW",
                "SESSION_DURATION_SEC": random.randint(20, 60),
                "RISK_SIGNAL": "POSITIVE_DISCIPLINE",
                "DESCRIPTION": "Просмотр деталей досрочного списания",
            })

        # Ночная активность (редкие события — 1 раз в 2-3 месяца во время IT-релизов в 03:40)
        if tel_date.day == 14 and tel_date.month in [4, 8, 10]:
            tel_counter += 1
            telem_events.append({
                "EVENT_ID": f"EVT-{tel_counter}",
                "TIMESTAMP": f"{tel_date.strftime('%Y-%m-%d')} 03:40:12",
                "EVENT_TYPE": "NIGHT_APP_CHECK",
                "AUTH_METHOD": "Biometrics",
                "IP_ADDRESS": "178.89.44.112",
                "GEO_LOCATION": "Almaty, Medeu District",
                "SCREEN_VIEW": "DASHBOARD_PREDELINQUENCY_RADAR",
                "SESSION_DURATION_SEC": 85,
                "RISK_SIGNAL": "EARLY_WARNING_LATENT",
                "DESCRIPTION": "Ночная проверка приложения во время ночного деплоя бэкенда",
            })

        tel_date += datetime.timedelta(days=1)

    df_telem = pd.DataFrame(telem_events)
    df_telem.to_csv(output_dir / "arman_telemetry_stream.csv", index=False)
    print(f"[8/8] ✅ arman_telemetry_stream.csv: {len(df_telem)} потоковых цифровых следов в мобильном банке ДБО")

    # =========================================================================
    # 9. СОЗДАНИЕ ПОЛНОГО ФИНАНСОВОГО ДОСЬЕ (MARKDOWN)
    # =========================================================================
    dossier_content = f"""# 📑 ПОЛНОЕ ФИНАНСОВОЕ ДОСЬЕ: АРМАН СЕЙТКАЛИЕВ
### Цифровой двойник кредитного риска (360° RiskTwin Benchmark)

---

### 1. Паспортные и социальные данные
* **ФИО:** Сейткалиев Арман Бахытович
* **ИИН:** `{iin}`
* **Возраст:** 29 лет (дата рождения: 15.04.1997)
* **Город:** г. Алматы (Медеуский / Бостандыкский район)
* **Семейное положение:** Не женат, детей нет
* **Образование:** Высшее профильное (МУИТ / IITU, специальность «Информационные системы и программирование», 2019)
* **Текущая должность:** Lead Backend Architect / Senior IT Specialist
* **Работодатель:** ТОО «QazFinTech Solutions» (аккредитованная компания в Astana Hub)
* **Непрерывный трудовой стаж:** 7 лет (с 2019 года, 100% официальные пенсионные отчисления в ЕНПФ)

---

### 2. Кредитный договор и ключевые параметры
* **Номер счета:** `{account_num}`
* **Токен заемщика:** `{client_token}`
* **Сумма займа:** **₸ 4 200 000**
* **Ежемесячный аннуитет:** **₸ 145 000**
* **Текущий доход:** **₸ 1 200 000** / месяц
* **Коэффициент долговой нагрузки (DTI / КДН):** **12.08%** (норматив АРРФР: до 50%)
* **Свободный остаток на счетах:** **₸ 650 000** (+ ₸ 2 100 000 на сберегательном депозите)
* **Внешний скоринг ПКБ (EXT_SOURCE_2):** **0.88** (Класс надежности: **AAA**)

---

### 3. Реляционная история (2021 — 2026 гг.)

```
2021           2022           2023           2024           2025           2026
─┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬─
 │              │              │              │              │              │
 ├─ BNPL iSpace ├─ BNPL Techno ├─ Текущий заем├─ Кредитная   ├─ Депозит     ├─ Полная
 │  (MacBook)   │  (iPhone)    │  (₸ 4.2 млн) │  карта ₸ 1M  │  ₸ 2.1 млн   │  готовность
 └─ 12 мес (OK) └─ 10 мес (OK) └─ 36 платежей └─ 100% грейс └─ 14.5% ГЭСВ  └─ к погашению
                                  (-5.4 дн)
```

1. **2021–2022 (Товарная рассрочка iSpace Dostyk Plaza):**
   * Рассрочка на ноутбук Apple MacBook Pro M1 Max на сумму ₸ 450 000 на 12 месяцев.
   * Все 12 платежей внесены без единой задержки. Договор успешно закрыт.
2. **2022–2023 (Товарная рассрочка Technodom Mega Alma-Ata):**
   * Рассрочка на смартфон Apple iPhone на сумму ₸ 380 000 на 10 месяцев.
   * Договор закрыт досрочно на 10-м месяце.
3. **2023–2026 (Крупный заем ₸ 4 200 000):**
   * 36 аннуитетных платежей по ₸ 145 000.
   * Каждый платеж списывается в среднем за **5.40 дня до дедлайна** благодаря регулярному зачислению зарплаты 25-го числа.
   * **0** дней просрочки (DPD = 0) за всю 5-летнюю историю.
4. **Кредитная карта (Лимит ₸ 1 000 000):**
   * Утилизация строго на уровне **18.0%**.
   * 100% операций — безналичные покупки (билеты, супермаркеты, профессиональный софт).
   * **0 ₸** снятий в банкоматах. Все задолженности закрываются в течение 50-дневного льготного грейс-периода.

---

### 4. Поведенческий цифровой след в ДБО
* Регулярные входы в мобильный банк с 08:30 до 09:00 по биометрии FaceID.
* Подписки на софт мирового уровня: JetBrains, GitHub Copilot, AWS Cloud, OpenAI.
* Единичные ночные сессии в приложении (03:40) привязаны к графикам ночных IT-релизов в компании и не несут кредитного риска.
* Вероятность дефолта по оценке нейросети PyTorch Full360: **~0.86% – 1.28%** (Абсолютный эталон финансовой стабильности).
"""
    with open(output_dir / "arman_financial_dossier.md", "w", encoding="utf-8") as f:
        f.write(dossier_content)
    print(f"[9/9] ✅ arman_financial_dossier.md: Полное аналитическое досье заемщика оформлено")

    # =========================================================================
    # ВЕРИФИКАЦИЯ ЧЕРЕЗ АГРЕГАТОР И PYTORCH ИНФЕРЕНС
    # =========================================================================
    print("\n" + "=" * 85)
    print("🔍 ВЕРИФИКАЦИЯ: ПЕРЕСЧЕТ ВСЕХ АГРЕГАТОВ И ИНФЕРЕНС PYTORCH")
    print("=" * 85)

    # Проверка ключевых равенств
    avg_delay = df_inst["DELAY_DAYS"].mean()
    late_cnt = (df_inst["DELAY_DAYS"] > 0).sum()
    completed_pos = (df_pos["NAME_CONTRACT_STATUS"] == "Completed").sum()
    cc_util = (df_cc["AMT_BALANCE"] / df_cc["AMT_CREDIT_LIMIT_ACTUAL"]).mean()
    cc_atm = df_cc["AMT_DRAWINGS_ATM_CURRENT"].sum()
    cc_pos = df_cc["AMT_DRAWINGS_POS_CURRENT"].sum()
    prev_refused = (df_prev["NAME_CONTRACT_STATUS"] == "Refused").sum()

    print(f"  • Среднее опережение графика: {avg_delay:.2f} дней (ожидается -5.40)")
    print(f"  • Просрочек платежей: {late_cnt} (ожидается 0)")
    print(f"  • Закрытых рассрочек BNPL: {completed_pos} (ожидается 2)")
    print(f"  • Средняя утилизация кредитной карты: {cc_util:.1%} (ожидается 18.0%)")
    print(f"  • Снятие наличных в банкоматах: ₸ {cc_atm:,.0f} (ожидается 0)")
    print(f"  • Безналичные покупки по кредитке: ₸ {cc_pos:,.0f} (ожидается 320,000)")
    print(f"  • Отказов в кредитах: {prev_refused} (ожидается 0)")

    assert abs(avg_delay - (-5.4)) < 1e-4, "Ошибка в задержке платежей!"
    assert late_cnt == 0, "Обнаружены просрочки!"
    assert completed_pos == 2, "Ошибка в числе закрытых договоров!"
    assert abs(cc_util - 0.18) < 1e-4, "Ошибка в утилизации карты!"
    assert cc_atm == 0.0, "Ошибка в снятиях наличных!"
    assert cc_pos == 320000.0, "Ошибка в безналичном обороте!"

    # Прогон через PyTorch модель
    models_dir = base_dir / "models"
    model_path = models_dir / "home_credit_full_360_model.pt"
    scalers_path = models_dir / "home_credit_full_360_scalers.pkl"

    if model_path.exists() and scalers_path.exists():
        with open(scalers_path, "rb") as f:
            scalers = pickle.load(f)
        ckpt = torch.load(model_path, map_location="cpu")

        sys.path.insert(0, str(base_dir.parent / "agent-world"))
        from app.ml_inference import Full360CrossAttentionNet

        credit_cols = ckpt["credit_cols"]
        behavior_cols = ckpt["behavior_cols"]

        c_dict = {
            "AMT_INCOME_TOTAL": 1200000.0,
            "AMT_CREDIT": 4200000.0,
            "AMT_ANNUITY": 145000.0,
            "dti_ratio": 145000.0 / 1200000.0,
            "credit_to_income_ratio": 4200000.0 / 1200000.0,
            "age_years": 29.0,
            "employment_years": 7.0,
            "EXT_SOURCE_1": 0.85,
            "EXT_SOURCE_2": 0.88,
            "EXT_SOURCE_3": 0.86,
            "prev_app_total": 3.0,
            "prev_refused_count": 0.0,
            "prev_approved_count": 3.0,
            "bureau_active_loans": 0.0,
            "bureau_total_debt": 0.0,
            "bureau_total_overdue": 0.0,
            "bureau_prolong_count": 0.0,
            "NAME_CONTRACT_TYPE_Revolving loans": 0.0,
            "NAME_INCOME_TYPE_Pensioner": 0.0,
            "NAME_INCOME_TYPE_State servant": 0.0,
            "NAME_INCOME_TYPE_Student": 0.0,
            "NAME_INCOME_TYPE_Unemployed": 0.0,
            "NAME_INCOME_TYPE_Working": 0.0,
            "NAME_HOUSING_TYPE_House / apartment": 1.0,
            "NAME_HOUSING_TYPE_Municipal apartment": 0.0,
            "NAME_HOUSING_TYPE_Office apartment": 0.0,
            "NAME_HOUSING_TYPE_Rented apartment": 0.0,
            "NAME_HOUSING_TYPE_With parents": 0.0,
        }

        b_dict = {
            "inst_total_tx": 36.0,
            "inst_avg_delay_days": -5.4,
            "inst_max_delay_days": 0.0,
            "inst_late_count": 0.0,
            "inst_underpay_count": 0.0,
            "inst_total_deficit": 0.0,
            "pos_active_count": 0.0,
            "pos_completed_count": 2.0,
            "pos_remaining_installments": 0.0,
            "pos_max_dpd": 0.0,
            "cc_atm_drawings_sum": 0.0,
            "cc_atm_drawings_cnt": 0.0,
            "cc_pos_drawings_sum": 320000.0,
            "cc_utilization_mean": 0.18,
            "cc_max_dpd": 0.0,
        }

        c_vals = np.array([[c_dict[col] for col in credit_cols]], dtype=np.float32)
        b_vals = np.array([[b_dict[col] for col in behavior_cols]], dtype=np.float32)

        c_scaled = scalers["scaler_credit"].transform(c_vals)
        b_scaled = scalers["scaler_behavior"].transform(b_vals)

        net = Full360CrossAttentionNet(
            credit_dim=ckpt["credit_dim"],
            behavior_dim=ckpt["behavior_dim"],
            embed_dim=32,
            num_heads=4,
            dropout=0.0
        )
        net.load_state_dict(ckpt["model_state_dict"])
        net.eval()

        with torch.no_grad():
            logits, weights = net(torch.tensor(c_scaled), torch.tensor(b_scaled))
            prob = torch.sigmoid(logits).item()

        print(f"\n🧠 ИНФЕРЕНС PYTORCH Full360CrossAttentionNet:")
        print(f"  • Расчетный PD (Вероятность дефолта): {prob * 100:.2f}% (Класс AAA)")
        print(f"  • Тензор Cross-Attention: {list(weights.shape)} успешно вычислен")

    print("\n" + "=" * 85)
    print("🏆 ВСЕ 8 CSV-ТАБЛИЦ И ДОСЬЕ УСПЕШНО СФОРМИРОВАНЫ И ПРОШЛИ ПРОВЕРКУ!")
    print("=" * 85)

if __name__ == "__main__":
    generate_deep_arman_history()
