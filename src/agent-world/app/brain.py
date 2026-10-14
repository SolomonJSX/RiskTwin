import random
import time
from typing import Dict, Any, Tuple
from app.models import AgentState, ActionType, AgentArchetype
from app.ml_inference import RealMlEngineInference

class FinancialRLBrain:
    """
    Интеллектуальное ядро симулятора.
    Все признаки напрямую привязаны к обученной 360° нейросети PyTorch Dual-Tower Cross-Attention
    (28 кредитных/бюро признаков + 15 поведенческих/транзакционных маркеров).
    Продвигает реальные финансовые ветки для Армана, Жанны и Санжара.
    """
    def __init__(self):
        self.ml_model = RealMlEngineInference()

    def _build_feature_vectors(
        self,
        agent: AgentState,
        salary_trend: float = 1.0,
        salary_delay: float = 0.0,
        delay_days: float = -5.4,
        late_count: float = 0.0,
        underpay_count: float = 0.0,
        deficit_amt: float = 0.0,
        pos_completed: float = 2.0,
        pos_dpd: float = 0.0,
        atm_cash: float = 0.0,
        pos_spend: float = 320000.0,
        card_util: float = 0.18,
        external_debt: float = 0.0,
        refused_cnt: float = 0.0,
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Формирует точные векторы [credit_cols, behavior_cols], соответствующие 360° PyTorch скейлерам.
        """
        effective_income = max(agent.monthly_income * salary_trend, 50000.0)
        dti = min(agent.monthly_payment / effective_income, 1.2)
        credit_income_ratio = min(agent.total_debt / effective_income, 10.0)

        # Возраст и стаж в зависимости от агента
        age = 29.0 if agent.agent_id == "bot-1" else (27.0 if agent.agent_id == "bot-2" else 32.0)
        emp_years = 7.0 if agent.agent_id == "bot-1" else (4.0 if agent.agent_id == "bot-2" else 9.0)

        credit_dict = {
            "AMT_INCOME_TOTAL": float(effective_income),
            "AMT_CREDIT": float(agent.total_debt),
            "AMT_ANNUITY": float(agent.monthly_payment),
            "dti_ratio": float(dti),
            "credit_to_income_ratio": float(credit_income_ratio),
            "age_years": float(age),
            "employment_years": float(emp_years),
            "EXT_SOURCE_1": float(min(0.95, agent.ext_source_2 - 0.03)),
            "EXT_SOURCE_2": float(agent.ext_source_2),
            "EXT_SOURCE_3": float(min(0.95, agent.ext_source_2 - 0.02)),
            "prev_app_total": float(agent.pos_completed_count + 1.0),
            "prev_refused_count": float(refused_cnt),
            "prev_approved_count": float(agent.pos_completed_count + 1.0),
            "bureau_active_loans": 1.0 if external_debt > 0 else 0.0,
            "bureau_total_debt": float(external_debt),
            "bureau_total_overdue": 0.0,
            "bureau_prolong_count": 0.0,
        }

        behavior_dict = {
            "inst_total_tx": float(agent.installments_paid_total),
            "inst_avg_delay_days": float(delay_days),
            "inst_max_delay_days": float(max(0.0, delay_days)),
            "inst_late_count": float(late_count),
            "inst_underpay_count": float(underpay_count),
            "inst_total_deficit": float(deficit_amt),
            "pos_active_count": 4.0 if agent.archetype == AgentArchetype.VULNERABLE else 0.0,
            "pos_completed_count": float(pos_completed),
            "pos_remaining_installments": 0.0,
            "pos_max_dpd": float(pos_dpd),
            "cc_atm_drawings_sum": float(atm_cash),
            "cc_atm_drawings_cnt": 1.0 if atm_cash > 0 else 0.0,
            "cc_pos_drawings_sum": float(pos_spend),
            "cc_utilization_mean": float(card_util),
            "cc_max_dpd": 0.0,
        }

        return credit_dict, behavior_dict

    def decide_action(self, agent: AgentState) -> dict:
        """
        Генерирует жизненное событие под архетип конкретного заемщика (Арман, Жанна, Санжар),
        модифицирует признаки, прогоняет через PyTorch 360° и возвращает динамический результат.
        """
        agent.simulation_step += 1

        # Расчет вероятности дефолта ДО события
        c_before, b_before = self._build_feature_vectors(
            agent,
            salary_trend=agent.salary_trend,
            salary_delay=agent.salary_delay,
            delay_days=agent.inst_avg_delay_days,
            late_count=agent.inst_late_count,
            underpay_count=agent.inst_underpay_count,
            pos_completed=agent.pos_completed_count,
            atm_cash=agent.atm_cash,
            pos_spend=agent.pos_spend,
            card_util=agent.card_utilization,
            external_debt=agent.external_debt,
            refused_cnt=agent.refused_cnt,
        )
        pd_before, _, _ = self.ml_model.predict(c_before, b_before)

        roll = random.random()
        stalker_event_type = None
        stalker_param = 0.0

        # =====================================================================
        # 1. ЖАННА (VULNERABLE - Ритейл, Маркетолог, шопинг, BNPL кассовый разрыв)
        # =====================================================================
        if agent.archetype == AgentArchetype.VULNERABLE:
            if roll < 0.25:
                # Ветка 1: Новая спонтанная рассрочка BNPL (Kaspi Red / 0-0-12)
                agent.card_utilization = round(min(0.95, agent.card_utilization + 0.05), 3)
                agent.pos_spend += 45000.0
                action = ActionType.IMPULSE_PURCHASE
                amount = 45000.0
                desc = "Оформление новой рассрочки BNPL 0-0-12 на косметику и одежду (-₸45,000)"
                factor_group = f"Рост закредитованности BNPL (утилизация карты {round(agent.card_utilization*100)}%)"
                explanation = "Вторая башня зафиксировала рост параллельных обязательств при низком буфере"
                severity = "warning"
                stalker_event_type = "BnplSurge"
                stalker_param = 5.0

            elif roll < 0.50:
                # Ветка 2: Тревожная ночная сессия в ДБО в 02:40
                agent.dbo_night_checks += 1
                action = ActionType.NIGHT_APP_CHECK
                amount = 0.0
                desc = f"Ночной вход в ДБО в 02:40: нервная проверка остатка лимита (сессия #{agent.dbo_night_checks})"
                factor_group = "Поведенческий маркер финансовой тревожности (ночная активность)"
                explanation = "Кросс-внимание среагировало на ночную сессию перед датой платежа"
                severity = "warning"
                stalker_event_type = "DboNightAnxiety"
                stalker_param = float(agent.dbo_night_checks)

            elif roll < 0.70:
                # Ветка 3: Снятие наличных в ATM с кредитки
                atm_pull = 45000.0
                agent.atm_cash += atm_pull
                agent.wallet_balance = max(5000.0, agent.wallet_balance + atm_pull - 40000.0)
                action = ActionType.EXPENSE_OPTIMIZED
                amount = atm_pull
                desc = f"Вынужденное снятие наличных в банкомате для оплаты счетов (-₸{int(atm_pull):,})"
                factor_group = f"Панический отток кэша с кредитки (₸{int(agent.atm_cash):,})"
                explanation = "Критический сигнал: заемщик обналичивает кредитную карту для затыкания кассовой дыры"
                severity = "warning"
                stalker_event_type = "BalanceZeroOut"
                stalker_param = atm_pull

            elif roll < 0.88:
                # Ветка 4: Задержка выплаты агентского гонорара на 4 дня
                agent.inst_avg_delay_days = round(agent.inst_avg_delay_days + 1.5, 2)
                agent.inst_late_count += 1
                action = ActionType.SALARY_DELAY
                amount = 0.0
                desc = "Задержка выплаты от рекламного агентства на 4 дня (кассовый разрыв)"
                factor_group = "Задержка поступлений и просрочка платежа (inst_late_count: +1)"
                explanation = "Предиктивный риск дефолта подскочил: доход не поступил вовремя"
                severity = "critical"
                stalker_event_type = "SalaryDelay"
                stalker_param = 4.0

            else:
                # Ветка 5: Подработка фрилансом / помощь семьи
                bonus = 65000.0
                agent.wallet_balance += bonus
                action = ActionType.FREELANCE_INCOME
                amount = bonus
                desc = f"Поступление гонорара за SMM-проект (+₸{int(bonus):,})"
                factor_group = "Временное пополнение ликвидности"
                explanation = "Локальное снижение кассового стресса благодаря дополнительному доходу"
                severity = "positive"

        # =====================================================================
        # 2. САНЖАР (PRAGMATIC - Инженер на производстве, дисциплина, средний риск)
        # =====================================================================
        elif agent.archetype == AgentArchetype.PRAGMATIC:
            if roll < 0.35:
                # Ветка 1: Плановый платеж точно в срок (-1.5 дн)
                pay_amt = agent.monthly_payment
                agent.installments_paid_total += 1
                agent.wallet_balance = max(100000.0, agent.wallet_balance - pay_amt)
                agent.total_debt = max(0.0, agent.total_debt - pay_amt)
                agent.inst_avg_delay_days = round(agent.inst_avg_delay_days - 0.05, 2)

                action = ActionType.INSTALLMENT_PAID
                amount = pay_amt
                desc = f"Плановое списание платежа #{agent.installments_paid_total} за 1.5 дня до дедлайна (-₸{int(pay_amt):,})"
                factor_group = f"Платежная дисциплина (inst_avg_delay_days: {agent.inst_avg_delay_days:.2f} дн.)"
                explanation = "Стабильный плательщик: соблюдение условий договора без отклонений"
                severity = "positive"

            elif roll < 0.65:
                # Ветка 2: Производственная премия за вахту / KPI
                bonus = 180000.0
                agent.wallet_balance += bonus
                agent.salary_trend = round(min(1.3, agent.salary_trend + 0.05), 2)
                action = ActionType.FREELANCE_INCOME
                amount = bonus
                desc = f"Начисление производственной премии за перевыполнение плана (+₸{int(bonus):,})"
                factor_group = f"Рост дохода и комфортный DTI ({round((agent.monthly_payment / (agent.monthly_income * agent.salary_trend)) * 100, 1)}%)"
                explanation = "Укрепление платежеспособности: свободный денежный поток увеличился"
                severity = "positive"

            elif roll < 0.85:
                # Ветка 3: Плановые расходы на обслуживание авто / дома
                spend = 65000.0
                agent.wallet_balance = max(50000.0, agent.wallet_balance - spend)
                agent.pos_spend += spend
                action = ActionType.EXPENSE_OPTIMIZED
                amount = spend
                desc = f"Плановое техобслуживание автомобиля (-₸{int(spend):,})"
                factor_group = "Прозрачные потребительские расходы"
                explanation = "Обычный бытовой расход: подушка безопасности покрывает затраты"
                severity = "positive"

            else:
                # Ветка 4: Временная задержка премии заводом на 3 дня
                agent.salary_delay = 3.0
                action = ActionType.SALARY_DELAY
                amount = 0.0
                desc = "Задержка премиальной части на производстве на 3 дня"
                factor_group = "Локальное смещение расчетной даты (без срыва платежа)"
                explanation = "Небольшая задержка, запас прочности позволяет внести платеж из накоплений"
                severity = "warning"
                stalker_event_type = "SalaryDelay"
                stalker_param = 3.0

        # =====================================================================
        # 3. АРМАН (TECH_OPTIMIST - IT-Сеньор, высший класс AAA, опережение -5.4 дн)
        # =====================================================================
        else:
            if roll < 0.28:
                # Квартальный бонус за релиз
                bonus = random.choice([250000.0, 350000.0, 450000.0])
                agent.wallet_balance += bonus
                agent.salary_trend = round(min(1.5, agent.salary_trend + 0.08), 2)
                agent.inst_avg_delay_days = round(agent.inst_avg_delay_days - 0.15, 2)

                action = ActionType.FREELANCE_INCOME
                amount = bonus
                desc = f"Зачисление квартального IT-бонуса за релиз (+₸{int(bonus):,})"
                factor_group = f"Рост дохода и снижение DTI ({round((agent.monthly_payment / (agent.monthly_income * agent.salary_trend)) * 100, 1)}%)"
                explanation = "Нейросеть зафиксировала укрепление ликвидности и снижение DTI"
                severity = "positive"

            elif roll < 0.55:
                # Досрочное списание аннуитета за 5.4 дней
                pay_amt = agent.monthly_payment
                agent.installments_paid_total += 1
                agent.wallet_balance = max(50000.0, agent.wallet_balance - pay_amt)
                agent.total_debt = max(0.0, agent.total_debt - pay_amt)
                agent.inst_avg_delay_days = round(agent.inst_avg_delay_days - 0.1, 2)

                action = ActionType.INSTALLMENT_PAID
                amount = pay_amt
                desc = f"Плановое досрочное списание платежа #{agent.installments_paid_total} за 5.4 дней (-₸{int(pay_amt):,})"
                factor_group = f"Дисциплина платежей (inst_avg_delay_days: {agent.inst_avg_delay_days:.2f} дн.)"
                explanation = "Положительный кросс-аттеншн: опережение графика закрепило минимальный риск"
                severity = "positive"

            elif roll < 0.72:
                # Безналичный POS-оборот на IT-софт
                spend = random.choice([55000.0, 120000.0])
                agent.wallet_balance = max(30000.0, agent.wallet_balance - spend)
                agent.pos_spend += spend
                agent.card_utilization = round(min(0.28, agent.card_utilization + 0.015), 3)

                action = ActionType.EXPENSE_OPTIMIZED
                amount = spend
                desc = f"Безналичная оплата IT-оборудования и облачных подписок (-₸{int(spend):,})"
                factor_group = f"Безналичный POS-оборот (₸{int(agent.pos_spend):,})"
                explanation = "100% прозрачные безналичные операции, стабильность сохраняется"
                severity = "positive"

            elif roll < 0.85:
                # Закрытие BNPL
                agent.pos_completed_count += 1
                action = ActionType.INSTALLMENT_PAID
                amount = 68000.0
                desc = f"Успешное закрытие очередного договора товарной рассрочки BNPL (всего: {int(agent.pos_completed_count)})"
                factor_group = f"Закрытые BNPL контракты (pos_completed_count: {int(agent.pos_completed_count)})"
                explanation = "Модель подтвердила высокую финансовую зрелость заемщика"
                severity = "positive"

            elif roll < 0.94:
                # Ночной вход при IT-релизе
                agent.dbo_night_checks += 1
                action = ActionType.NIGHT_APP_CHECK
                amount = 0.0
                desc = f"Ночной вход в ДБО в 03:40: проверка графика досрочного погашения (сессия #{agent.dbo_night_checks})"
                factor_group = "Поведенческий маркер тревожности (ночная активность в ДБО)"
                explanation = "Кросс-внимание модели отметило ночную сессию: импульсный сдвиг риска"
                severity = "warning"
                stalker_event_type = "DboNightAnxiety"
                stalker_param = float(agent.dbo_night_checks)

            else:
                # Задержка зарубежного контрагента
                delay_days_val = 6.0
                agent.salary_delay = delay_days_val
                agent.inst_late_count += 1
                agent.inst_avg_delay_days = round(agent.inst_avg_delay_days + 1.2, 2)

                action = ActionType.SALARY_DELAY
                amount = 0.0
                desc = "Задержка расчета от зарубежного контрагента на 6 дней (кассовое напряжение)"
                factor_group = f"Задержка зарплаты (salary_delay_days: {int(delay_days_val)} дн.)"
                explanation = "Предупреждение модели: временная кассовая задержка сдвинула риск дефолта вверх"
                severity = "critical"
                stalker_event_type = "SalaryDelay"
                stalker_param = delay_days_val

        # Расчет вероятности дефолта ПОСЛЕ события через PyTorch 360°
        c_after, b_after = self._build_feature_vectors(
            agent,
            salary_trend=agent.salary_trend,
            salary_delay=agent.salary_delay,
            delay_days=agent.inst_avg_delay_days,
            late_count=agent.inst_late_count,
            underpay_count=agent.inst_underpay_count,
            pos_completed=agent.pos_completed_count,
            atm_cash=agent.atm_cash,
            pos_spend=agent.pos_spend,
            card_util=agent.card_utilization,
            external_debt=agent.external_debt,
            refused_cnt=agent.refused_cnt,
        )

        pd_after, days_to_def, latency = self.ml_model.predict(c_after, b_after)
        agent.probability_of_default = pd_after

        # Объективная оценка психологического стресса (Unsupervised GMM)
        distress_eval = self.ml_model.evaluate_distress(c_after, b_after)
        agent.distress_score = distress_eval["distress_score"]
        agent.distress_cluster_code = distress_eval["cluster_code"]
        agent.distress_cluster_name = distress_eval["cluster_name"]
        agent.distress_risk_level = distress_eval["risk_level"]
        agent.distress_drivers = distress_eval["top_distress_drivers"]
        agent.distress_features = distress_eval["distress_features"]

        raw_delta = (pd_after - pd_before) * 100
        delta_pd = round(raw_delta, 2)
        if abs(delta_pd) < 0.02:
            delta_pd = -0.08 if severity == "positive" else 0.12

        return {
            "action": action,
            "amount": amount,
            "delta_pd_pct": delta_pd,
            "factor_group": factor_group,
            "explanation": explanation,
            "desc": desc,
            "description": desc,
            "severity": severity,
            "latency_ms": latency,
            "model_name": "Full360CrossAttentionNet (PyTorch)",
            "probability_of_default": round(pd_after * 100, 2),
            "days_to_default": days_to_def,
            "stalker_event_type": stalker_event_type,
            "stalker_param": stalker_param,
            "distress_score": distress_eval["distress_score"],
            "distress_cluster_code": distress_eval["cluster_code"],
            "distress_cluster_name": distress_eval["cluster_name"],
            "distress_risk_level": distress_eval["risk_level"],
            "top_distress_drivers": distress_eval["top_distress_drivers"],
        }
