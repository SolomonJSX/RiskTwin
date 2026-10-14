'use client';

import React, { useState, useEffect } from 'react';
import {
  Brain,
  Activity,
  AlertTriangle,
  ShieldCheck,
  Zap,
  TrendingDown,
  DollarSign,
  CreditCard,
  RotateCcw,
  Sparkles,
  HelpCircle,
  Users
} from 'lucide-react';
import { HumanoidStressAvatar3D } from './HumanoidStressAvatar3D';

interface DistressAgent {
  agent_id: string;
  name: string;
  role: string;
  avatar: string;
  monthly_income: number;
  wallet_balance: number;
  monthly_payment: number;
  total_debt: number;
  distress_score: number;
  distress_cluster_code: string;
  distress_cluster_name: string;
  distress_risk_level: string;
  distress_features: {
    cash_panic_ratio?: number;
    payment_delay_distress?: number;
    deficit_burden_ratio?: number;
    rejection_desperation_rate?: number;
    bnpl_fragmentation_burden?: number;
    bureau_shock_severity?: number;
  };
  top_distress_drivers: Array<{
    feature: string;
    name: string;
    value: number;
    impact: number;
  }>;
}

const DEFAULT_AGENTS: DistressAgent[] = [
  {
    agent_id: 'bot-1',
    name: 'Арман (IT-Сеньор)',
    role: 'Lead Software Engineer',
    avatar: '👨‍💻',
    monthly_income: 1200000,
    wallet_balance: 650000,
    monthly_payment: 145000,
    total_debt: 4200000,
    distress_score: 0.05,
    distress_cluster_code: 'STABLE_DISCIPLINE',
    distress_cluster_name: 'Финансовая устойчивость и самоконтроль',
    distress_risk_level: 'LOW',
    distress_features: {
      cash_panic_ratio: 0.0,
      payment_delay_distress: 0.0,
      deficit_burden_ratio: 0.12,
      rejection_desperation_rate: 0.0,
      bnpl_fragmentation_burden: 1.8,
      bureau_shock_severity: 0.0,
    },
    top_distress_drivers: [],
  },
  {
    agent_id: 'bot-2',
    name: 'Жанна (Маркетолог)',
    role: 'Digital Marketer / SMM Lead',
    avatar: '👩‍💼',
    monthly_income: 420000,
    wallet_balance: 45000,
    monthly_payment: 185000,
    total_debt: 2600000,
    distress_score: 0.68,
    distress_cluster_code: 'ACUTE_PANIC',
    distress_cluster_name: 'Острая паника: обналичивание кредиток и отказы',
    distress_risk_level: 'HIGH_EARLY_WARNING',
    distress_features: {
      cash_panic_ratio: 48.5,
      payment_delay_distress: 0.15,
      deficit_burden_ratio: 0.78,
      rejection_desperation_rate: 0.65,
      bnpl_fragmentation_burden: 4.2,
      bureau_shock_severity: 1.4,
    },
    top_distress_drivers: [
      {
        feature: 'cash_panic_ratio',
        name: 'Паническое обналичивание кредиток в банкоматах',
        value: 48.5,
        impact: 48.5,
      },
      {
        feature: 'rejection_desperation_rate',
        name: 'Веерная подача заявок и серия отказов в займах',
        value: 0.65,
        impact: 0.58,
      },
      {
        feature: 'bnpl_fragmentation_burden',
        name: 'Перегрузка товарными рассрочками (BNPL)',
        value: 4.2,
        impact: 1.21,
      },
    ],
  },
  {
    agent_id: 'bot-3',
    name: 'Санжар (Инженер)',
    role: 'Plant Chief Engineer',
    avatar: '👷‍♂️',
    monthly_income: 850000,
    wallet_balance: 420000,
    monthly_payment: 160000,
    total_debt: 3800000,
    distress_score: 0.28,
    distress_cluster_code: 'LATENT_ANXIETY',
    distress_cluster_name: 'Латентная тревожность и дробление рассрочек',
    distress_risk_level: 'MODERATE',
    distress_features: {
      cash_panic_ratio: 0.0,
      payment_delay_distress: 0.0,
      deficit_burden_ratio: 0.45,
      rejection_desperation_rate: 0.15,
      bnpl_fragmentation_burden: 3.1,
      bureau_shock_severity: 0.0,
    },
    top_distress_drivers: [
      {
        feature: 'deficit_burden_ratio',
        name: 'Хронический кассовый разрыв и дефицит',
        value: 0.45,
        impact: 0.23,
      },
    ],
  },
];

export const StressTwinDashboard: React.FC = () => {
  const [agents, setAgents] = useState<DistressAgent[]>(DEFAULT_AGENTS);
  const [selectedAgentId, setSelectedAgentId] = useState<string>('bot-2');
  const [liveSimRunning, setLiveSimRunning] = useState<boolean>(false);

  // Загрузка реальных агентов из agent-world API
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await fetch('http://localhost:8001/api/world/agents');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setAgents(data);
          }
        }
      } catch {
        // Fallback на дефолтных агентов
      }
    };

    fetchAgents();
    const interval = setInterval(fetchAgents, 3500);
    return () => clearInterval(interval);
  }, []);

  const currentAgent = agents.find((a) => a.agent_id === selectedAgentId) || agents[0];

  // Симуляция интерактивных стресс-шоков "Что если"
  const applyShock = (type: string) => {
    setAgents((prev) =>
      prev.map((a) => {
        if (a.agent_id !== selectedAgentId) return a;

        let newScore = a.distress_score;
        let newCluster = a.distress_cluster_code;
        let newClusterName = a.distress_cluster_name;
        let newRisk = a.distress_risk_level;
        const newFeats = { ...a.distress_features };

        if (type === 'SALARY_DELAY') {
          newFeats.payment_delay_distress = (newFeats.payment_delay_distress || 0) + 0.45;
          newFeats.deficit_burden_ratio = (newFeats.deficit_burden_ratio || 0) + 0.35;
          newScore = Math.min(0.95, newScore + 0.22);
        } else if (type === 'CASH_PANIC') {
          newFeats.cash_panic_ratio = (newFeats.cash_panic_ratio || 0) + 65.0;
          newScore = Math.min(0.98, newScore + 0.35);
        } else if (type === 'MFO_REJECTION') {
          newFeats.rejection_desperation_rate = Math.min(1.0, (newFeats.rejection_desperation_rate || 0) + 0.5);
          newFeats.bureau_shock_severity = (newFeats.bureau_shock_severity || 0) + 2.0;
          newScore = Math.min(0.96, newScore + 0.25);
        } else if (type === 'AUTOPAY_FAIL') {
          newFeats.payment_delay_distress = (newFeats.payment_delay_distress || 0) + 0.6;
          newScore = Math.min(0.95, newScore + 0.18);
        } else if (type === 'RESET_STABILITY') {
          newFeats.cash_panic_ratio = 0.0;
          newFeats.payment_delay_distress = 0.0;
          newFeats.deficit_burden_ratio = 0.1;
          newFeats.rejection_desperation_rate = 0.0;
          newFeats.bureau_shock_severity = 0.0;
          newScore = 0.05;
        }

        if (newScore < 0.25) {
          newCluster = 'STABLE_DISCIPLINE';
          newClusterName = 'Финансовая устойчивость и самоконтроль';
          newRisk = 'LOW';
        } else if (newScore < 0.5) {
          newCluster = 'LATENT_ANXIETY';
          newClusterName = 'Латентная тревожность и дробление рассрочек';
          newRisk = 'MODERATE';
        } else if (newScore < 0.75) {
          newCluster = 'ACUTE_PANIC';
          newClusterName = 'Острая паника: обналичивание кредиток и отказы';
          newRisk = 'HIGH_EARLY_WARNING';
        } else {
          newCluster = 'CHRONIC_EXHAUSTION';
          newClusterName = 'Хроническое истощение и дефолтный коллапс';
          newRisk = 'CRITICAL';
        }

        return {
          ...a,
          distress_score: newScore,
          distress_cluster_code: newCluster,
          distress_cluster_name: newClusterName,
          distress_risk_level: newRisk,
          distress_features: newFeats,
        };
      })
    );
  };

  const getClusterBadgeColor = (code: string) => {
    switch (code) {
      case 'STABLE_DISCIPLINE':
        return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40';
      case 'LATENT_ANXIETY':
        return 'bg-amber-500/20 text-amber-400 border-amber-500/40';
      case 'ACUTE_PANIC':
        return 'bg-rose-500/20 text-rose-400 border-rose-500/40';
      case 'CHRONIC_EXHAUSTION':
        return 'bg-purple-500/20 text-purple-400 border-purple-500/40';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/40';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* 1. ВЕРХНИЙ ХЕДЕР И БЕНЧМАРК */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-3xl bg-slate-900/90 border border-emerald-500/30 backdrop-blur-xl shadow-2xl">
        <div className="flex items-center space-x-4">
          <div className="flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 text-white shadow-lg shadow-emerald-500/20">
            <Brain className="w-8 h-8" />
          </div>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-black text-white tracking-tight">
                3D Цифровой Психо-Двойник Заемщика
              </h1>
              <span className="px-2.5 py-1 text-xs font-bold rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
                Unsupervised GMM Core
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Биоповеденческий мониторинг стресса на основе 163 517 реальных заемщиков Home Credit • Без искусственных эвристик
            </p>
          </div>
        </div>

        {/* Выбор цифрового двойника */}
        <div className="flex items-center space-x-2 bg-slate-800/80 p-1.5 rounded-2xl border border-slate-700/60">
          {agents.map((agent) => (
            <button
              key={agent.agent_id}
              onClick={() => setSelectedAgentId(agent.agent_id)}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all ${
                selectedAgentId === agent.agent_id
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30 font-bold'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <span className="text-base">{agent.avatar || '👤'}</span>
              <span>{agent.name.split(' ')[0]}</span>
            </button>
          ))}
        </div>
      </div>

      {/* 2. ГЛАВНАЯ СЕКЦИЯ: 3D АВАТАР И ДАТА-ДРИВЕН МЕТРИКИ */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* ЛЕВАЯ КОЛОНКА (7/12): 3D Интерактивная фигура */}
        <div className="lg:col-span-7 flex flex-col space-y-4">
          <div className="relative rounded-3xl overflow-hidden border border-slate-800 bg-slate-950 p-2 shadow-2xl h-[520px]">
            <HumanoidStressAvatar3D
              distressScore={currentAgent.distress_score}
              clusterCode={currentAgent.distress_cluster_code}
            />
          </div>

          {/* Плашка описания текущего состояния */}
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{currentAgent.avatar || '👤'}</span>
              <div>
                <h3 className="text-sm font-bold text-white">{currentAgent.name}</h3>
                <p className="text-xs text-slate-400">{currentAgent.role}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="text-right">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Психологический статус</span>
                <span className={`inline-block px-2.5 py-0.5 text-xs font-bold rounded-lg border ${getClusterBadgeColor(currentAgent.distress_cluster_code)}`}>
                  {currentAgent.distress_cluster_name}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* ПРАВАЯ КОЛОНКА (5/12): ОБЪЕКТИВНЫЕ ДАННЫЕ СТРЕССА */}
        <div className="lg:col-span-5 flex flex-col space-y-4">
          {/* Индикатор уровня дистресса */}
          <div className="p-5 rounded-3xl bg-slate-900/90 border border-slate-800 backdrop-blur-xl">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Общий индекс поведенческого стресса
              </span>
              <span className="text-lg font-black text-white font-mono">
                {Math.round(currentAgent.distress_score * 100)}%
              </span>
            </div>

            {/* Прогресс-бар с цветовым градиентом */}
            <div className="w-full h-3.5 bg-slate-800 rounded-full overflow-hidden p-0.5 border border-white/5">
              <div
                className={`h-full rounded-full transition-all duration-700 ${
                  currentAgent.distress_score > 0.75
                    ? 'bg-gradient-to-r from-purple-500 to-rose-600'
                    : currentAgent.distress_score > 0.5
                    ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                    : currentAgent.distress_score > 0.25
                    ? 'bg-gradient-to-r from-emerald-500 to-amber-500'
                    : 'bg-emerald-500'
                }`}
                style={{ width: `${Math.max(5, currentAgent.distress_score * 100)}%` }}
              />
            </div>

            <div className="flex justify-between text-[10px] text-slate-400 font-mono mt-2">
              <span>0% Спокойствие</span>
              <span>50% Паника</span>
              <span>100% Истощение</span>
            </div>
          </div>

          {/* 6 Объективных факторов из Home Credit */}
          <div className="p-5 rounded-3xl bg-slate-900/90 border border-slate-800 flex-1 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Объективные транзакционные маркеры</span>
              </h4>
              <span className="text-[10px] text-slate-400 font-mono">Home Credit 360°</span>
            </div>

            <div className="space-y-2.5 text-xs">
              {/* 1. Cash Panic */}
              <div className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">Паническое снятие в банкоматах</p>
                  <p className="text-[10px] text-slate-400">cash_panic_ratio • Обналичивание кредиток</p>
                </div>
                <span className={`font-mono font-bold px-2 py-0.5 rounded text-xs ${
                  (currentAgent.distress_features?.cash_panic_ratio || 0) > 10 ? 'bg-rose-500/20 text-rose-300' : 'bg-slate-700 text-slate-300'
                }`}>
                  {(currentAgent.distress_features?.cash_panic_ratio || 0).toFixed(1)}
                </span>
              </div>

              {/* 2. Payment Delay */}
              <div className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">Задержки и сбои дисциплины</p>
                  <p className="text-[10px] text-slate-400">payment_delay_distress • DPD & Late Tx</p>
                </div>
                <span className={`font-mono font-bold px-2 py-0.5 rounded text-xs ${
                  (currentAgent.distress_features?.payment_delay_distress || 0) > 0.2 ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-700 text-slate-300'
                }`}>
                  {(currentAgent.distress_features?.payment_delay_distress || 0).toFixed(2)}
                </span>
              </div>

              {/* 3. Deficit Burden */}
              <div className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">Хронический кассовый разрыв</p>
                  <p className="text-[10px] text-slate-400">deficit_burden_ratio • Дефицит к аннуитету</p>
                </div>
                <span className="font-mono font-bold px-2 py-0.5 rounded text-xs bg-slate-700 text-slate-300">
                  {(currentAgent.distress_features?.deficit_burden_ratio || 0).toFixed(2)}
                </span>
              </div>

              {/* 4. Rejection Desperation */}
              <div className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">Веерные заявки и серия отказов</p>
                  <p className="text-[10px] text-slate-400">rejection_desperation_rate • Фрустрация</p>
                </div>
                <span className={`font-mono font-bold px-2 py-0.5 rounded text-xs ${
                  (currentAgent.distress_features?.rejection_desperation_rate || 0) > 0.3 ? 'bg-rose-500/20 text-rose-300' : 'bg-slate-700 text-slate-300'
                }`}>
                  {(currentAgent.distress_features?.rejection_desperation_rate || 0).toFixed(2)}
                </span>
              </div>

              {/* 5. BNPL Fragmentation */}
              <div className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/40 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">Перегрузка рассрочками BNPL</p>
                  <p className="text-[10px] text-slate-400">bnpl_fragmentation_burden • Дробление долга</p>
                </div>
                <span className="font-mono font-bold px-2 py-0.5 rounded text-xs bg-slate-700 text-slate-300">
                  {(currentAgent.distress_features?.bnpl_fragmentation_burden || 0).toFixed(1)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 3. ИНТЕРАКТИВНЫЙ СИМУЛЯТОР СТРЕСС-ШОКОВ "ЧТО ЕСЛИ" */}
      <div className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Zap className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white">
              Интерактивный Симулятор Стресс-Шоков «Что если»
            </h3>
          </div>
          <span className="text-xs text-slate-400">
            Нажимайте кнопки для мгновенной симуляции финансового стресса на 3D аватаре
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <button
            onClick={() => applyShock('SALARY_DELAY')}
            className="flex flex-col items-center p-3.5 rounded-2xl bg-slate-800/80 hover:bg-amber-600/20 border border-amber-500/30 text-amber-200 transition-all text-xs font-semibold group text-center"
          >
            <TrendingDown className="w-5 h-5 mb-1.5 text-amber-400 group-hover:scale-110 transition-transform" />
            <span>Задержка зарплаты</span>
            <span className="text-[10px] text-slate-400 mt-0.5">+10 дней задержки</span>
          </button>

          <button
            onClick={() => applyShock('CASH_PANIC')}
            className="flex flex-col items-center p-3.5 rounded-2xl bg-slate-800/80 hover:bg-rose-600/20 border border-rose-500/30 text-rose-200 transition-all text-xs font-semibold group text-center"
          >
            <DollarSign className="w-5 h-5 mb-1.5 text-rose-400 group-hover:scale-110 transition-transform" />
            <span>Паника в банкомате</span>
            <span className="text-[10px] text-slate-400 mt-0.5">Снятие 150 000 ₸ с кредитки</span>
          </button>

          <button
            onClick={() => applyShock('MFO_REJECTION')}
            className="flex flex-col items-center p-3.5 rounded-2xl bg-slate-800/80 hover:bg-purple-600/20 border border-purple-500/30 text-purple-200 transition-all text-xs font-semibold group text-center"
          >
            <AlertTriangle className="w-5 h-5 mb-1.5 text-purple-400 group-hover:scale-110 transition-transform" />
            <span>Отказы в займах</span>
            <span className="text-[10px] text-slate-400 mt-0.5">Веерные заявки в МФО</span>
          </button>

          <button
            onClick={() => applyShock('AUTOPAY_FAIL')}
            className="flex flex-col items-center p-3.5 rounded-2xl bg-slate-800/80 hover:bg-red-600/20 border border-red-500/30 text-red-200 transition-all text-xs font-semibold group text-center"
          >
            <CreditCard className="w-5 h-5 mb-1.5 text-red-400 group-hover:scale-110 transition-transform" />
            <span>Сбой автоплатежа</span>
            <span className="text-[10px] text-slate-400 mt-0.5">Нехватка остатка</span>
          </button>

          <button
            onClick={() => applyShock('RESET_STABILITY')}
            className="flex flex-col items-center p-3.5 rounded-2xl bg-emerald-950/60 hover:bg-emerald-800/40 border border-emerald-500/40 text-emerald-200 transition-all text-xs font-semibold group text-center col-span-2 sm:col-span-1"
          >
            <RotateCcw className="w-5 h-5 mb-1.5 text-emerald-400 group-hover:scale-110 transition-transform" />
            <span>Стабилизация</span>
            <span className="text-[10px] text-emerald-400/80 mt-0.5">Сброс в STABLE</span>
          </button>
        </div>
      </div>
    </div>
  );
};
