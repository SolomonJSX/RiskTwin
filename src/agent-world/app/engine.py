import asyncio
import datetime
import uuid
import random
import subprocess
from typing import List, Dict, Any, Optional
import httpx
from app.models import AgentState, AgentArchetype
from app.brain import FinancialRLBrain

class AgentWorldEngine:
    def __init__(self, backend_url: str = "http://localhost:5000"):
        self.backend_url = backend_url
        self.brain = FinancialRLBrain()
        self.is_running = False
        self.tick_speed = 2.5
        self.event_counter = 0
        self.agent_cursor = 0
        self.agents: List[AgentState] = self._init_agents()
        self.live_logs: List[Dict[str, Any]] = []

    def _init_agents(self) -> List[AgentState]:
        return [
            # 1. АРМАН (Класс AAA - Высшая надежность)
            AgentState(
                agent_id="bot-1",
                name="Арман (IT-Сеньор)",
                role="Lead Software Engineer",
                avatar="👨‍💻",
                archetype=AgentArchetype.TECH_OPTIMIST,
                monthly_income=1200000.0,
                wallet_balance=650000.0,
                monthly_payment=145000.0,
                total_debt=4200000.0,
                account_number="KZ886010002003004001",
                client_token="11111111-2222-3333-4444-555555555555",
                probability_of_default=0.0105,
                ext_source_2=0.88,
                days_to_payment=18,
                salary_trend=1.0,
                salary_delay=0.0,
                inst_avg_delay_days=-5.4,
                inst_late_count=0.0,
                inst_underpay_count=0.0,
                pos_completed_count=2.0,
                pos_spend=320000.0,
                atm_cash=0.0,
                card_utilization=0.18,
                installments_paid_total=36
            ),
            # 2. ЖАННА (Класс BBB - Кассовый разрыв / BNPL-нагрузка)
            AgentState(
                agent_id="bot-2",
                name="Жанна (Маркетолог)",
                role="Digital Marketer / SMM Lead",
                avatar="👩‍💼",
                archetype=AgentArchetype.VULNERABLE,
                monthly_income=420000.0,
                wallet_balance=45000.0,
                monthly_payment=185000.0,
                total_debt=2600000.0,
                account_number="KZ886010002003004002",
                client_token="22222222-3333-4444-5555-666666666666",
                probability_of_default=0.168,
                ext_source_2=0.58,
                days_to_payment=7,
                salary_trend=1.0,
                salary_delay=0.0,
                inst_avg_delay_days=2.4,
                inst_late_count=3.0,
                inst_underpay_count=0.0,
                pos_completed_count=1.0,
                pos_spend=210000.0,
                atm_cash=85000.0,
                card_utilization=0.82,
                dbo_night_checks=5,
                installments_paid_total=14
            ),
            # 3. САНЖАР (Класс AA - Прагматичный инженер на производстве)
            AgentState(
                agent_id="bot-3",
                name="Санжар (Инженер)",
                role="Plant Chief Engineer",
                avatar="👷‍♂️",
                archetype=AgentArchetype.PRAGMATIC,
                monthly_income=850000.0,
                wallet_balance=420000.0,
                monthly_payment=160000.0,
                total_debt=3800000.0,
                account_number="KZ886010002003004003",
                client_token="33333333-4444-5555-6666-777777777777",
                probability_of_default=0.048,
                ext_source_2=0.76,
                days_to_payment=14,
                salary_trend=1.0,
                salary_delay=0.0,
                inst_avg_delay_days=-1.5,
                inst_late_count=0.0,
                inst_underpay_count=0.0,
                pos_completed_count=3.0,
                pos_spend=140000.0,
                atm_cash=0.0,
                card_utilization=0.12,
                installments_paid_total=24
            ),
        ]

    async def step(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Квант симуляции с продвижением реальных веток признаков и PyTorch инференсом"""
        if agent_id:
            agent = next((a for a in self.agents if a.agent_id == agent_id or a.account_number == agent_id), self.agents[0])
        else:
            # Чередуем агентов или выбираем циклично
            agent = self.agents[self.agent_cursor % len(self.agents)]
            self.agent_cursor += 1

        agent.days_to_payment = max(1, agent.days_to_payment - 1)

        # РЕАЛЬНЫЙ РАСЧЕТ И ПРОДВИЖЕНИЕ ПО ВЕТКЕ
        decision = self.brain.decide_action(agent)

        self.event_counter += 1
        now_str = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "id": f"evt-{self.event_counter}-{uuid.uuid4().hex[:6]}",
            "timestamp": now_str,
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "role": agent.role,
            "avatar": agent.avatar,
            "account_number": agent.account_number,
            "action": decision["action"].value,
            "amount": decision["amount"],
            "delta_pd_pct": decision["delta_pd_pct"],
            "factor_group": decision["factor_group"],
            "explanation": decision["explanation"],
            "description": decision["desc"],
            "severity": decision["severity"],
            "latency_ms": decision.get("latency_ms", 12.0),
            "model_name": decision.get("model_name", "Full360CrossAttentionNet"),
            "wallet_balance": round(agent.wallet_balance, 2),
            "probability_of_default": round(agent.probability_of_default * 100, 2),
            "dti_ratio": round((agent.monthly_payment / max(1.0, agent.monthly_income * agent.salary_trend)) * 100, 1),
            "inst_avg_delay_days": round(agent.inst_avg_delay_days, 2),
            "pos_completed_count": int(agent.pos_completed_count),
            "card_utilization": round(agent.card_utilization * 100, 1),
            "simulation_step": agent.simulation_step,
            "distress_score": round(agent.distress_score, 4),
            "distress_cluster_code": agent.distress_cluster_code,
            "distress_cluster_name": agent.distress_cluster_name,
            "distress_risk_level": agent.distress_risk_level,
            "top_distress_drivers": agent.distress_drivers,
        }

        agent.history.append(log_entry)
        self.live_logs.insert(0, log_entry)
        if len(self.live_logs) > 60:
            self.live_logs.pop()

        # Асинхронно синхронизируем PostgreSQL
        asyncio.create_task(self._sync_event_to_db(agent, decision, log_entry))

        return log_entry

    async def _sync_event_to_db(self, agent: AgentState, decision: dict, log_entry: dict):
        # 1. Попытка уведомить backend (.NET Stalker API)
        stalker_type = decision.get("stalker_event_type")
        if stalker_type:
            try:
                async with httpx.AsyncClient(timeout=1.5) as client:
                    await client.post(
                        f"{self.backend_url}/api/Stalker/simulate-event",
                        json={
                            "clientToken": agent.client_token,
                            "eventType": stalker_type,
                            "amount": float(decision.get("amount", 0)),
                            "merchantOrRecipient": f"[{agent.name}] {decision['desc']}",
                            "delayDays": int(decision.get("stalker_param", 0)) if stalker_type == "SalaryDelay" else 0,
                            "metadata": f"{decision['factor_group']} • {decision['explanation']}"
                        }
                    )
            except Exception:
                pass

        # 2. Прямая синхронизация в PostgreSQL
        try:
            evt_id = f"EVT-LIVE-{self.event_counter}"
            desc_safe = decision["desc"].replace("'", "''")
            factor_safe = decision["factor_group"].replace("'", "''")
            pd_val = agent.probability_of_default
            dti_val = (agent.monthly_payment / max(1.0, agent.monthly_income * agent.salary_trend))

            sql = f"""
            INSERT INTO stalker_timeline_snapshots (
                snapshot_id, client_token, timestamp, risk_score, delta_pd, salary_trend, salary_delay_days,
                has_mfo_activity, active_bnpl_count, dti_estimate, daily_balance_7d, dbo_checks_count, primary_trigger
            ) VALUES (
                gen_random_uuid(), '{agent.client_token}', NOW(), {pd_val}, {decision["delta_pd_pct"] / 100.0},
                {agent.salary_trend}, {int(agent.salary_delay)}, false, {4 if agent.archetype == AgentArchetype.VULNERABLE else 0}, {dti_val},
                {agent.wallet_balance}, {agent.dbo_night_checks}, '{factor_safe}'
            );

            UPDATE client_profiles
            SET current_risk_score = {pd_val},
                risk_level = CASE WHEN {pd_val} > 0.40 THEN 'RED' WHEN {pd_val} > 0.15 THEN 'YELLOW' ELSE 'GREEN' END,
                updated_at = NOW()
            WHERE client_token = '{agent.client_token}';
            """

            subprocess.Popen(
                ["docker", "exec", "-i", "risktwin-postgres", "psql", "-U", "risktwin_user", "-d", "risktwin_db"],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            ).communicate(input=sql.encode("utf-8"))
        except Exception:
            pass
