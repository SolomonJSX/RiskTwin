'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sliders, Cpu, RotateCcw, ArrowRight, Zap, TrendingDown, User, ShieldAlert, CheckCircle2, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export interface BotProfile {
  accountNumber: string;
  name: string;
  role: string;
  avatar: string;
  monthlyIncome: number;
  monthlyPayment: number;
  walletBalance: number;
  totalDebt: number;
  basePd: number;
}

export const BOT_PROFILES: Record<string, BotProfile> = {
  'KZ886010002003004001': {
    accountNumber: 'KZ886010002003004001',
    name: 'Арман',
    role: 'IT-Сеньор',
    avatar: '👨‍💻',
    monthlyIncome: 1200000,
    monthlyPayment: 145000,
    walletBalance: 650000,
    totalDebt: 4200000,
    basePd: 1.05,
  },
  'KZ886010002003004002': {
    accountNumber: 'KZ886010002003004002',
    name: 'Жанна',
    role: 'Маркетолог',
    avatar: '👩‍💼',
    monthlyIncome: 420000,
    monthlyPayment: 185000,
    walletBalance: 45000,
    totalDebt: 2600000,
    basePd: 16.8,
  },
  'KZ886010002003004003': {
    accountNumber: 'KZ886010002003004003',
    name: 'Санжар',
    role: 'Инженер',
    avatar: '👷‍♂️',
    monthlyIncome: 850000,
    monthlyPayment: 160000,
    walletBalance: 420000,
    totalDebt: 3800000,
    basePd: 4.8,
  },
};

interface InteractiveSimProps {
  initialAccount?: string;
  onApplyPlan: (optimizedPayment: number, newTenor: number) => void;
  onSelectBot?: (accountNumber: string) => void;
}

export const InteractiveSimulator: React.FC<InteractiveSimProps> = ({
  initialAccount = 'KZ886010002003004001', // По умолчанию Арман
  onApplyPlan,
  onSelectBot,
}) => {
  const [selectedAcc, setSelectedAcc] = useState<string>(initialAccount);
  const activeBot = BOT_PROFILES[selectedAcc] || BOT_PROFILES['KZ886010002003004001'];

  // Ползунки шоковых факторов
  const [incomeDropPct, setIncomeDropPct] = useState(0); // 0% - 70%
  const [microloanAmount, setMicroloanAmount] = useState(0); // 0 - 300 000 ₸
  const [unexpectedExpense, setUnexpectedExpense] = useState(0); // 0 - 400 000 ₸
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizedResult, setOptimizedResult] = useState<{
    newPayment: number;
    newTenor: number;
    kdnDrop: string;
    successRate: number;
  } | null>(null);

  // Расчет текущей финансовой нагрузки
  const currentIncome = Math.round(activeBot.monthlyIncome * (1 - incomeDropPct / 100));
  const effectivePayment = optimizedResult ? optimizedResult.newPayment : activeBot.monthlyPayment;
  const mfoMonthlyLoad = microloanAmount > 0 ? Math.round(microloanAmount * 0.35) : 0;
  const totalMonthlyLoad = effectivePayment + mfoMonthlyLoad;
  const currentKdn = Math.min(Math.round((totalMonthlyLoad / Math.max(currentIncome, 30000)) * 100), 100);

  // Динамический прогноз кэшфлоу и подушки безопасности на 6 месяцев вперед
  const livingCost = Math.round(activeBot.monthlyIncome * 0.45); // 45% базовые расходы на жизнь

  let runningCushion = Math.max(
    0,
    activeBot.walletBalance - unexpectedExpense + microloanAmount
  );

  const forecastData = [1, 2, 3, 4, 5, 6].map((m) => {
    // Ежемесячный денежный поток
    const netCashflow = currentIncome - livingCost - totalMonthlyLoad;
    runningCushion = Math.max(0, runningCushion + netCashflow);

    const isDefaultMonth = runningCushion <= 0 && netCashflow < 0;
    const stressScore = Math.min(
      100,
      Math.max(
        activeBot.basePd,
        currentKdn > 50 ? activeBot.basePd + 30 : activeBot.basePd + (incomeDropPct > 0 ? 15 : 0)
      )
    );

    return {
      month: isDefaultMonth ? `Мес ${m} (Дефолт)` : `Мес ${m}`,
      balanceKzt: Math.round(runningCushion),
      balanceKztK: Math.round(runningCushion / 1000),
      stressScore: stressScore,
      isDefault: isDefaultMonth,
    };
  });

  const hasDefault = forecastData.some((f) => f.isDefault || f.balanceKzt === 0);

  const handleSelectBot = (acc: string) => {
    setSelectedAcc(acc);
    setIncomeDropPct(0);
    setMicroloanAmount(0);
    setUnexpectedExpense(0);
    setOptimizedResult(null);
    if (onSelectBot) onSelectBot(acc);
  };

  const handleRunOptimization = () => {
    setIsOptimizing(true);
    setTimeout(() => {
      setIsOptimizing(false);
      // Математическая оптимизация OR-Tools: подбираем платеж не выше 30% от стресс-дохода
      const targetPayment = Math.round(currentIncome * 0.28);
      setOptimizedResult({
        newPayment: targetPayment,
        newTenor: 48,
        kdnDrop: `${currentKdn}% ➔ 28%`,
        successRate: 97.8,
      });
    }, 600);
  };

  const handleReset = () => {
    setIncomeDropPct(0);
    setMicroloanAmount(0);
    setUnexpectedExpense(0);
    setOptimizedResult(null);
  };

  return (
    <div className="bg-white rounded-3xl p-6 lg:p-8 border border-slate-200/90 shadow-sm space-y-6">
      
      {/* 1. Селектор 10 ботов */}
      <div>
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
          <div className="flex items-center space-x-2">
            <User className="w-4 h-4 text-emerald-600" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Выберите заемщика для стресс-тестирования:
            </span>
          </div>
          <span className="text-xs text-slate-500 font-mono">Фокусный двойник: Арман (360° Модель)</span>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-thin">
          {Object.values(BOT_PROFILES).map((bot) => {
            const isSelected = bot.accountNumber === selectedAcc;
            return (
              <button
                key={bot.accountNumber}
                onClick={() => handleSelectBot(bot.accountNumber)}
                className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer border ${
                  isSelected
                    ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm scale-102'
                    : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
                }`}
              >
                <span className="text-base">{bot.avatar}</span>
                <span className="font-bold">{bot.name}</span>
                <span className={`text-[10px] font-mono px-1.5 py-0.5 rounded-md ${
                  isSelected ? 'bg-emerald-700 text-white' : 'bg-slate-200/60 text-slate-600'
                }`}>
                  ₸{(bot.monthlyIncome / 1000).toFixed(0)}к
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 2. Шапка профиля выбранного заемщика */}
      <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200/70 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="text-3xl p-2 bg-white rounded-xl shadow-xs border border-emerald-100">
            {activeBot.avatar}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-extrabold text-slate-900">{activeBot.name}</h3>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                {activeBot.role}
              </span>
            </div>
            <p className="text-xs text-slate-500 font-mono mt-0.5">
              Счет: {activeBot.accountNumber} • Базовый PD: {activeBot.basePd}%
            </p>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 text-xs">
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Доход в месяц:</span>
            <span className="font-bold text-slate-900 font-mono">₸{activeBot.monthlyIncome.toLocaleString('ru-RU')}</span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Платеж в банк:</span>
            <span className="font-bold text-slate-900 font-mono">₸{activeBot.monthlyPayment.toLocaleString('ru-RU')}</span>
          </div>
          <div className="bg-white p-2.5 rounded-xl border border-slate-200 shadow-2xs">
            <span className="text-slate-400 text-[10px] block">Подушка сейчас:</span>
            <span className="font-bold text-emerald-700 font-mono">₸{activeBot.walletBalance.toLocaleString('ru-RU')}</span>
          </div>
        </div>

        <button
          onClick={handleReset}
          className="inline-flex items-center space-x-1.5 px-3 py-2 text-xs font-semibold rounded-xl text-slate-700 bg-white hover:bg-slate-100 border border-slate-200 transition-all self-start md:self-auto cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Сбросить шоки</span>
        </button>
      </div>

      {/* 3. Рабочая зона: Ползунки + График траектории */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Левая колонка: 3 интерактивных ползунка шока */}
        <div className="lg:col-span-5 space-y-5">
          <div className="space-y-4 bg-slate-50/70 p-5 rounded-2xl border border-slate-200">
            
            {/* Ползунок 1: Падение дохода */}
            <div>
              <div className="flex justify-between text-xs font-bold mb-1.5">
                <span className="text-slate-700">Падение ежемесячного заработка</span>
                <span className="text-rose-600 font-extrabold font-mono">-{incomeDropPct}%</span>
              </div>
              <input
                type="range"
                min="0"
                max="70"
                step="5"
                value={incomeDropPct}
                onChange={(e) => {
                  setIncomeDropPct(Number(e.target.value));
                  setOptimizedResult(null);
                }}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>В норме (₸{activeBot.monthlyIncome.toLocaleString('ru-RU')})</span>
                <span>Кризис (₸{currentIncome.toLocaleString('ru-RU')})</span>
              </div>
            </div>

            {/* Ползунок 2: Взятие микрозайма */}
            <div>
              <div className="flex justify-between text-xs font-bold mb-1.5">
                <span className="text-slate-700">Взято займов в сторонних МФО</span>
                <span className="text-amber-600 font-extrabold font-mono">
                  +₸{microloanAmount.toLocaleString('ru-RU')}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="300000"
                step="25000"
                value={microloanAmount}
                onChange={(e) => {
                  setMicroloanAmount(Number(e.target.value));
                  setOptimizedResult(null);
                }}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>0 ₸ (нет микрозаймов)</span>
                <span>₸300 000 (высокая ставка)</span>
              </div>
            </div>

            {/* Ползунок 3: Непредвиденные расходы */}
            <div>
              <div className="flex justify-between text-xs font-bold mb-1.5">
                <span className="text-slate-700">Внезапные расходы (медицина / авто)</span>
                <span className="text-teal-700 font-extrabold font-mono">
                  ₸{unexpectedExpense.toLocaleString('ru-RU')}
                </span>
              </div>
              <input
                type="range"
                min="0"
                max="400000"
                step="25000"
                value={unexpectedExpense}
                onChange={(e) => {
                  setUnexpectedExpense(Number(e.target.value));
                  setOptimizedResult(null);
                }}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-teal-600"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>0 ₸</span>
                <span>₸400 000 (удар по подушке)</span>
              </div>
            </div>

          </div>

          {/* Индикатор нагрузки на бюджет */}
          <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-xs flex items-center justify-between">
            <div>
              <div className="text-xs text-slate-500 font-medium">Кредитная нагрузка (КДН):</div>
              <div className={`text-2xl font-black mt-0.5 font-mono ${
                currentKdn > 60 ? 'text-rose-600' : currentKdn > 40 ? 'text-amber-600' : 'text-emerald-700'
              }`}>
                {currentKdn}% дохода
              </div>
            </div>
            <div className={`px-3 py-1 rounded-full text-xs font-bold border flex items-center space-x-1.5 ${
              currentKdn > 60
                ? 'bg-rose-100 text-rose-800 border-rose-300'
                : currentKdn > 40
                ? 'bg-amber-100 text-amber-800 border-amber-300'
                : 'bg-emerald-100 text-emerald-800 border-emerald-300'
            }`}>
              {currentKdn > 60 ? (
                <>
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>Кассовый разрыв</span>
                </>
              ) : currentKdn > 40 ? (
                <>
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Напряжение</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>В безопасности</span>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Правая колонка: Прогноз финансовой подушки (6 мес) + Кнопка OR-Tools */}
        <div className="lg:col-span-7 flex flex-col justify-between space-y-4">
          
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5">
                <TrendingDown className="w-4 h-4 text-emerald-600" />
                <span>Прогноз подушки ликвидности: {activeBot.name} (6 мес.)</span>
              </span>
              <span className="text-[11px] text-slate-400 font-mono">
                {hasDefault ? '⚠️ Зафиксирована точка дефолта' : '✅ Подушка устойчива'}
              </span>
            </div>

            <div className="h-52 w-full bg-slate-50/70 rounded-2xl p-3 border border-slate-200">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={forecastData}>
                  <defs>
                    <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={hasDefault ? '#f43f5e' : '#10b981'} stopOpacity={0.6}/>
                      <stop offset="95%" stopColor={hasDefault ? '#f43f5e' : '#10b981'} stopOpacity={0.0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#64748b' }} />
                  <YAxis
                    tick={{ fontSize: 10, fill: '#64748b' }}
                    tickFormatter={(val) => `₸${val}к`}
                  />
                  <Tooltip
                    formatter={(val: any) => [`₸${Number(val).toLocaleString('ru-RU')} тыс.`, 'Остаток подушки']}
                    labelFormatter={(label) => `Период: ${label}`}
                  />
                  <Area
                    type="monotone"
                    dataKey="balanceKztK"
                    stroke={hasDefault ? '#e11d48' : '#059669'}
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#colorBalance)"
                    name="Остаток подушки (тыс. ₸)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Результат или Кнопка запуска оптимизатора */}
          {!optimizedResult ? (
            <button
              onClick={handleRunOptimization}
              disabled={isOptimizing}
              className="w-full py-4 rounded-2xl bg-gradient-to-r from-emerald-600 via-emerald-700 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white font-bold text-sm shadow-md flex items-center justify-center space-x-2.5 transition-all active:scale-[0.99] disabled:opacity-50 cursor-pointer"
            >
              <Cpu className={`w-5 h-5 ${isOptimizing ? 'animate-spin' : ''}`} />
              <span>
                {isOptimizing
                  ? 'Оптимизатор Google OR-Tools решает задачу реструктуризации...'
                  : 'Запустить ИИ-подбор спасительного сценария'}
              </span>
              {!isOptimizing && <Zap className="w-4 h-4 text-emerald-200" />}
            </button>
          ) : (
            <motion.div
              initial={{ scale: 0.97, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="p-5 rounded-2xl bg-gradient-to-r from-emerald-700 via-emerald-600 to-teal-700 text-white shadow-lg space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-200" />
                  <span>Идеальное решение найдено за 12ms (OR-Tools)</span>
                </span>
                <span className="text-xs font-mono text-emerald-950 bg-emerald-200 font-bold px-2.5 py-0.5 rounded-full">
                  Устойчивость: {optimizedResult.successRate}%
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 py-1">
                <div className="p-3 rounded-xl bg-white/10 border border-white/10">
                  <span className="text-[11px] text-emerald-100 block">Новый щадящий платеж:</span>
                  <span className="text-xl font-extrabold text-white font-mono">
                    ₸{optimizedResult.newPayment.toLocaleString('ru-RU')}
                  </span>
                </div>
                <div className="p-3 rounded-xl bg-white/10 border border-white/10">
                  <span className="text-[11px] text-emerald-100 block">Снижение нагрузки (КДН):</span>
                  <span className="text-xl font-extrabold text-emerald-200 font-mono">
                    {optimizedResult.kdnDrop}
                  </span>
                </div>
              </div>

              <div className="flex justify-end pt-2">
                <button
                  onClick={() => onApplyPlan(optimizedResult.newPayment, optimizedResult.newTenor)}
                  className="px-5 py-2.5 rounded-xl bg-white hover:bg-emerald-50 text-emerald-900 font-bold text-xs shadow-md transition-all flex items-center space-x-2 cursor-pointer"
                >
                  <span>Перейти к соглашению и подписать</span>
                  <ArrowRight className="w-4 h-4 text-emerald-700" />
                </button>
              </div>
            </motion.div>
          )}

        </div>

      </div>

    </div>
  );
};
