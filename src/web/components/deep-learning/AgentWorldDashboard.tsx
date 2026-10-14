'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Play, Pause, FastForward, TrendingDown, TrendingUp, ShieldAlert, Cpu, Activity, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const AGENT_API = 'http://localhost:8001/api/world';

const BOT_AVATARS: Record<string, string> = {
  'KZ886010002003004001': '👨‍💻',
  'KZ886010002003004002': '👩‍💼',
  'KZ886010002003004003': '👷‍♂️',
};

interface AgentInfo {
  agent_id: string;
  name: string;
  archetype: string;
  monthly_income: number;
  wallet_balance: number;
  monthly_payment: number;
  total_debt: number;
  account_number: string;
  probability_of_default: number; // 0% - 100%
  days_to_payment: number;
}

interface WorldEvent {
  id: string;
  timestamp: string;
  agent_name: string;
  account_number: string;
  action: string;
  amount: number;
  delta_pd_pct: number;
  factor_group: string;
  explanation: string;
  description: string;
  severity: 'positive' | 'warning' | 'critical';
  latency_ms: number;
  model_name: string;
  wallet_balance: number;
  probability_of_default: number;
}

export const AgentWorldDashboard: React.FC = () => {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [events, setEvents] = useState<WorldEvent[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<AgentInfo | null>(null);

  const fetchWorld = async () => {
    try {
      const [agentsRes, eventsRes, statusRes] = await Promise.all([
        axios.get(`${AGENT_API}/agents`),
        axios.get(`${AGENT_API}/events`),
        axios.get(`${AGENT_API}/status`),
      ]);
      setAgents(agentsRes.data);
      setEvents(eventsRes.data);
      setIsRunning(statusRes.data.is_running);
    } catch (e) {
      // Игнорируем если сервер выключен
    }
  };

  useEffect(() => {
    fetchWorld();
    const interval = setInterval(fetchWorld, 1200);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    await axios.post(`${AGENT_API}/start?speed=2.0`);
    setIsRunning(true);
  };

  const handlePause = async () => {
    await axios.post(`${AGENT_API}/pause`);
    setIsRunning(false);
  };

  const handleStep = async () => {
    await axios.post(`${AGENT_API}/step`);
    fetchWorld();
  };

  return (
    <div className="space-y-6">
      
      {/* Шапка аналитического центра - чистый лаконичный стиль */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-3 flex-wrap">
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              Автономный мир цифровых двойников (Арман, Жанна, Санжар)
            </h2>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 whitespace-nowrap">
              <Cpu className="w-3.5 h-3.5 text-emerald-600" />
              <span>PyTorch Neural Net</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700 border border-slate-200 whitespace-nowrap">
              <span className={`w-2 h-2 rounded-full ${isRunning ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'}`} />
              <span>{isRunning ? 'Симуляция активна' : 'На паузе'}</span>
            </span>
          </div>
          <p className="text-xs text-slate-500">
            RL-моделирование: двухбашенная нейросеть с Cross-Attention вычисляет риск (PD) на каждом шаге (инференс ~12ms)
          </p>
        </div>

        {/* Панель управления - аккуратные кнопки в едином стиле */}
        <div className="flex items-center gap-2.5 flex-shrink-0">
          {!isRunning ? (
            <button
              onClick={handleStart}
              className="h-10 px-5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-sm active:scale-95 whitespace-nowrap cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>Запустить симуляцию</span>
            </button>
          ) : (
            <button
              onClick={handlePause}
              className="h-10 px-5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-semibold text-xs flex items-center gap-2 transition-all shadow-sm active:scale-95 whitespace-nowrap cursor-pointer"
            >
              <Pause className="w-3.5 h-3.5 fill-white" />
              <span>Пауза</span>
            </button>
          )}

          <button
            onClick={handleStep}
            className="h-10 px-4 rounded-xl bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 hover:border-slate-300 font-semibold text-xs flex items-center gap-1.5 transition-all shadow-2xs whitespace-nowrap active:scale-95 cursor-pointer"
            title="Один шаг симуляции"
          >
            <FastForward className="w-3.5 h-3.5 text-emerald-600" />
            <span>+1 шаг</span>
          </button>
        </div>
      </div>

      {/* Шкала интерпретации рисков (чистые контрастные карточки) */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-white border border-emerald-200/80 shadow-2xs text-xs">
          <span className="font-bold text-emerald-700 flex items-center space-x-1.5 text-xs">
            <TrendingDown className="w-4 h-4 text-emerald-600" />
            <span>Снижение риска (ΔPD: -3% ... -8%)</span>
          </span>
          <p className="text-slate-600 text-[11px] mt-1 font-normal">Фриланс, помощь семьи, плановое погашение рассрочки</p>
        </div>

        <div className="p-4 rounded-xl bg-white border border-amber-200/80 shadow-2xs text-xs">
          <span className="font-bold text-amber-700 flex items-center space-x-1.5 text-xs">
            <TrendingUp className="w-4 h-4 text-amber-600" />
            <span>Умеренный риск (ΔPD: +6% ... +14%)</span>
          </span>
          <p className="text-slate-600 text-[11px] mt-1 font-normal">Ночные входы в ДБО, задержка зарплаты, отказ автоплатежа</p>
        </div>

        <div className="p-4 rounded-xl bg-white border border-rose-200/80 shadow-2xs text-xs">
          <span className="font-bold text-rose-700 flex items-center space-x-1.5 text-xs">
            <ShieldAlert className="w-4 h-4 text-rose-600" />
            <span>Критический риск (ΔPD: +26%)</span>
          </span>
          <p className="text-slate-600 text-[11px] mt-1 font-normal">Оформление займа в МФО: сигнал мгновенного кассового разрыва</p>
        </div>
      </div>

      {/* Сетка 10 ботов + Живой лог */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Карточки 10 ботов */}
        <div className="lg:col-span-8 grid grid-cols-1 sm:grid-cols-2 gap-4">
          {agents.map((agent) => {
            const isDanger = agent.probability_of_default > 50;
            const isWarning = agent.probability_of_default > 25 && agent.probability_of_default <= 50;
            const avatar = BOT_AVATARS[agent.account_number] || '👤';

            return (
              <motion.div
                key={agent.agent_id}
                whileHover={{ y: -2 }}
                onClick={() => setSelectedAgent(agent)}
                className={`p-4 rounded-2xl transition-all cursor-pointer bg-white relative shadow-xs ${
                  isDanger
                    ? 'border-2 border-rose-300 ring-2 ring-rose-100 hover:border-rose-400'
                    : isWarning
                    ? 'border-2 border-amber-300 ring-2 ring-amber-100 hover:border-amber-400'
                    : 'border border-slate-200 hover:border-emerald-400'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-xl">{avatar}</span>
                    <div>
                      <span className="font-bold text-sm text-slate-900 block leading-tight">{agent.name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">{agent.account_number}</span>
                    </div>
                  </div>
                  <span className="text-[10px] font-medium px-2 py-0.5 rounded-full border border-slate-200 bg-slate-50 text-slate-600">
                    {agent.archetype}
                  </span>
                </div>

                <div className={`p-3 rounded-xl my-2.5 flex items-center justify-between border ${
                  isDanger
                    ? 'bg-rose-50/70 border-rose-200'
                    : isWarning
                    ? 'bg-amber-50/70 border-amber-200'
                    : 'bg-emerald-50/60 border-emerald-200'
                }`}>
                  <div>
                    <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider block">
                      Вероятность дефолта (PD):
                    </span>
                    <span className={`text-2xl font-black font-mono tracking-tight ${
                      isDanger ? 'text-rose-600' : isWarning ? 'text-amber-600' : 'text-emerald-700'
                    }`}>
                      {agent.probability_of_default}%
                    </span>
                  </div>

                  <div className="text-right">
                    <span className="text-slate-500 text-[10px] uppercase font-bold tracking-wider block">
                      Статус:
                    </span>
                    <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${
                      isDanger
                        ? 'bg-rose-100 text-rose-800 border-rose-300'
                        : isWarning
                        ? 'bg-amber-100 text-amber-800 border-amber-300'
                        : 'bg-emerald-100 text-emerald-800 border-emerald-300'
                    }`}>
                      {isDanger ? 'Критично' : isWarning ? 'Внимание' : 'Стабилен'}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs py-1">
                  <div>
                    <span className="text-slate-500 text-[10px] block">Баланс кошелька:</span>
                    <span className="font-mono font-bold text-slate-800">
                      ₸{agent.wallet_balance.toLocaleString('ru-RU')}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[10px] block">До платежа:</span>
                    <span className="font-mono font-semibold text-slate-800">
                      {agent.days_to_payment} дн.
                    </span>
                  </div>
                </div>

                <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden mt-2 border border-slate-200/50">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isDanger ? 'bg-rose-500' : isWarning ? 'bg-amber-500' : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.min(agent.probability_of_default, 100)}%` }}
                  />
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Живая лента нейро-вычислений - чистый белый контейнер */}
        <div className="lg:col-span-4 rounded-2xl p-5 bg-white border border-slate-200 shadow-sm flex flex-col h-[650px]">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center space-x-1.5">
              <Activity className="w-4 h-4 text-emerald-600" />
              <span>Поток нейро-выводов (PyTorch)</span>
            </span>
            <span className="text-[10px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full border border-slate-200">
              {events.length} событий
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 pr-1">
            <AnimatePresence initial={false}>
              {events.map((evt, idx) => {
                const isPositive = evt.delta_pd_pct < 0;

                return (
                  <motion.div
                    key={`${evt.id}-${evt.timestamp}-${idx}`}
                    initial={{ opacity: 0, x: -6 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0 }}
                    className={`p-3.5 rounded-xl border text-xs shadow-2xs ${
                      isPositive
                        ? 'bg-emerald-50/50 border-emerald-200'
                        : evt.delta_pd_pct > 20
                        ? 'bg-rose-50/50 border-rose-200'
                        : 'bg-amber-50/50 border-amber-200'
                    }`}
                  >
                    <div className="flex items-center justify-between text-[11px] mb-1.5">
                      <span className="font-bold text-slate-900">{evt.agent_name}</span>
                      <span className={`font-mono font-bold px-2 py-0.5 rounded-md border text-xs ${
                        isPositive
                          ? 'bg-emerald-100 text-emerald-800 border-emerald-300'
                          : 'bg-rose-100 text-rose-800 border-rose-300'
                      }`}>
                        ΔPD: {isPositive ? `${evt.delta_pd_pct}%` : `+${evt.delta_pd_pct}%`}
                      </span>
                    </div>

                    <p className="text-slate-800 font-medium leading-relaxed mb-2">
                      {evt.description}
                    </p>

                    <div className="p-2.5 rounded-lg bg-white border border-slate-200 text-[11px] space-y-0.5 shadow-2xs">
                      <div className="text-emerald-700 font-bold">{evt.factor_group}</div>
                      <div className="text-slate-600">{evt.explanation}</div>
                    </div>

                    {/* Реальные метаданные инференса модели */}
                    <div className="flex justify-between items-center text-[10px] text-slate-500 mt-2 font-mono border-t border-slate-100 pt-1.5">
                      <span className="flex items-center space-x-1 text-emerald-700 font-medium">
                        <Zap className="w-3 h-3 text-emerald-600" />
                        <span>PyTorch • {evt.latency_ms}ms</span>
                      </span>
                      <span className="text-slate-600 font-semibold">PD: {evt.probability_of_default}%</span>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </div>

      </div>

    </div>
  );
};
