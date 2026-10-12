import random
import time
from typing import Dict, Any


def generate_mock_transaction(client_token: str, crisis_mode: bool = False) -> Dict[str, Any]:
    """Генерирует событие банковской транзакции (CDC/Event stream)."""
    now = time.time()

    if crisis_mode:
        # Паттерн кризиса: ночные P2P переводы, МФО, агрессивный вывод кэша
        is_mfo = random.random() < 0.40
        is_p2p = random.random() < 0.65
        is_atm = random.random() < 0.30
        amount = random.choice([25000.0, 50000.0, 100000.0, 150000.0])
        tx_type = "ATM_CASHOUT" if is_atm else ("P2P_OUTFLOW" if is_p2p else "EXPENSE")
    else:
        # Нормальный паттерн: бытовые покупки, супермаркеты, редкие P2P
        is_mfo = False
        is_p2p = random.random() < 0.15
        is_atm = random.random() < 0.05
        amount = round(random.uniform(1500.0, 25000.0), 2)
        tx_type = "SUPERMARKET" if not is_p2p else "P2P_TRANSFER"

    return {
        "event_id": f"tx_{int(now * 1000)}_{random.randint(100, 999)}",
        "client_token": client_token,
        "amount": amount,
        "type": tx_type,
        "is_mfo_or_gambling": is_mfo,
        "is_atm_cash_out": is_atm,
        "is_p2p_transfer": is_p2p,
        "timestamp": now,
    }


def generate_mock_telemetry(client_token: str, crisis_mode: bool = False) -> Dict[str, Any]:
    """Генерирует событие цифровой телеметрии приложения ДБО."""
    now = time.time()

    if crisis_mode:
        # Всплеск тревожности: ночные заходы, зависание на экране долга
        return {
            "client_token": client_token,
            "night_dbo_login": True,
            "balance_check_frequency_surge": round(random.uniform(3.5, 6.0), 2),
            "loan_schedule_screen_dwell_time": round(random.uniform(90.0, 180.0), 1),
            "timestamp": now,
        }
    else:
        return {
            "client_token": client_token,
            "night_dbo_login": False,
            "balance_check_frequency_surge": round(random.uniform(0.8, 1.3), 2),
            "loan_schedule_screen_dwell_time": round(random.uniform(5.0, 20.0), 1),
            "timestamp": now,
        }
