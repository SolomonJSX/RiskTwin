import time
from typing import Dict, Any, List
import redis


class SlidingWindowAggregator:
    """
    Потоковый агрегатор признаков реального времени на базе Redis.
    Использует ZSET для расчета 7- и 30-дневных скользящих окон сумм и частот.
    Хранит готовый вектор в HASH client:{client_token}:features для мгновенного чтения O(1).
    """

    def __init__(self, r_client: redis.Redis):
        self.r = r_client

    def process_transaction_event(self, event: Dict[str, Any]):
        token = event["client_token"]
        amount = float(event["amount"])
        tx_type = event.get("type", "EXPENSE")
        is_mfo = bool(event.get("is_mfo_or_gambling", False))
        is_atm = bool(event.get("is_atm_cash_out", False))
        is_p2p = bool(event.get("is_p2p_transfer", False))
        now = time.time()

        # 1. Запись транзакции в Sorted Set (ZSET) для скользящего окна
        tx_key = f"feat:{token}:tx_history"
        self.r.zadd(tx_key, {f"{now}:{amount}:{tx_type}:{int(is_mfo)}:{int(is_p2p)}": now})

        # 2. Очистка транзакций старше 30 дней (30 * 86400 сек)
        horizon_30d = now - (30 * 86400)
        self.r.zremrangebyscore(tx_key, 0, horizon_30d)

        # 3. Скользящие расчеты по актуальным элементам
        recent_txs = self.r.zrange(tx_key, 0, -1)
        horizon_7d = now - (7 * 86400)

        p2p_7d, p2p_30d = 0.0, 0.0
        atm_sum, total_expense = 0.0, 0.0
        has_mfo = False
        inflows_30d, outflows_30d = 0.0, 0.0

        for item in recent_txs:
            item_str = item.decode("utf-8") if isinstance(item, bytes) else str(item)
            parts = item_str.split(":")
            if len(parts) >= 5:
                ts = float(parts[0])
                amt = float(parts[1])
                t_type = parts[2]
                mfo_flag = bool(int(parts[3]))
                p2p_flag = bool(int(parts[4]))

                if mfo_flag:
                    has_mfo = True

                if t_type == "INCOME":
                    inflows_30d += amt
                else:
                    outflows_30d += amt
                    total_expense += amt
                    if p2p_flag:
                        p2p_30d += amt
                        if ts >= horizon_7d:
                            p2p_7d += amt
                    if "ATM" in t_type:
                        atm_sum += amt

        # Метрики ликвидности
        atm_ratio = round(atm_sum / max(1.0, total_expense), 3)
        margin = round((inflows_30d - outflows_30d) / max(1.0, inflows_30d + outflows_30d), 3)

        # 4. Атомарное обновление HASH признаков клиента
        feat_key = f"client:{token}:features"
        pipe = self.r.pipeline()
        pipe.hset(feat_key, "p2p_outflow_sum_7d", str(round(p2p_7d, 2)))
        pipe.hset(feat_key, "p2p_outflow_sum_30d", str(round(p2p_30d, 2)))
        pipe.hset(feat_key, "atm_cash_out_intensity", str(atm_ratio))
        pipe.hset(feat_key, "net_cashflow_margin_30d", str(margin))
        if has_mfo:
            pipe.hset(feat_key, "mfo_gambling_tag_presence", "1")
        pipe.execute()

    def process_telemetry_event(self, event: Dict[str, Any]):
        token = event["client_token"]
        feat_key = f"client:{token}:features"

        updates = {}
        if "night_dbo_login" in event and event["night_dbo_login"]:
            current_logins = int(self.r.hget(feat_key, "microloan_calculator_views") or 0)
            updates["microloan_calculator_views"] = str(current_logins + 1)

        if "balance_check_frequency_surge" in event:
            updates["balance_check_frequency_surge"] = str(round(float(event["balance_check_frequency_surge"]), 2))

        if "loan_schedule_screen_dwell_time" in event:
            updates["loan_schedule_screen_dwell_time"] = str(round(float(event["loan_schedule_screen_dwell_time"]), 1))

        if updates:
            self.r.hset(feat_key, mapping=updates)
