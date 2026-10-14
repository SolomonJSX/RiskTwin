'use client';

import React from 'react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { User, Sparkles, AlertCircle, ArrowUpRight, ArrowDownRight, ShieldCheck, Zap, History } from 'lucide-react';

interface BotTwinViewProps {
  name: string;
  role: string;
  avatar: string;
  accountNumber: string;
  clientToken: string;
  riskProbability: number; // 0 - 100
  monthlyPayment: number;
  currentPrincipal: number;
  onEvaluate: () => void;
  isEvaluating: boolean;
  onOpenAgentWorld: () => void;
  onOpenHistory?: () => void;
}

export const BotTwinView: React.FC<BotTwinViewProps> = ({
  name,
  role,
  avatar,
  accountNumber,
  clientToken,
  riskProbability,
  monthlyPayment,
  currentPrincipal,
  onEvaluate,
  isEvaluating,
  onOpenAgentWorld,
  onOpenHistory,
}) => {
  const isHighRisk = riskProbability > 50;
  const isMediumRisk = riskProbability > 25 && riskProbability <= 50;

  // 4 оси финансового здоровья
  const radarData = [
    { subject: 'Стабильность дохода', value: Math.max(15, 100 - riskProbability * 0.9) },
    { subject: 'Комфорт платежа', value: Math.max(20, 100 - riskProbability * 0.8) },
    { subject: 'Кредитная дисциплина', value: Math.max(10, 100 - riskProbability * 1.1) },
    { subject: 'Подушка безопасности', value: Math.max(15, 100 - riskProbability * 1.0) },
  ];

  return (
    <div className="glass-card rounded-3xl p-6 lg:p-8 bg-white border border-slate-200/80 shadow-md">
      
      {/* Шапка карточки двойника */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-50 border border-emerald-200/60 flex items-center justify-center text-3xl shadow-xs">
            {avatar}
          </div>
          <div>
            <div className="flex items-center space-x-2.5">
              <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                {name} <span className="text-sm font-semibold text-slate-500">({role})</span>
              </h2>
              <span className="px-2.5 py-0.5 text-xs font-bold bg-emerald-100 text-emerald-800 rounded-full border border-emerald-200">
                Цифровой двойник 360°
              </span>
              <span className="hidden sm:inline-block px-2.5 py-0.5 text-[11px] font-semibold bg-slate-100 text-slate-700 rounded-full border border-slate-200">
                {riskProbability < 5 ? 'Класс AAA • Минимальный риск' : riskProbability <= 15 ? 'Класс AA • Стабильный' : 'Класс BBB • Пред-дефолтный риск'}
              </span>
            </div>
            <p className="text-xs text-slate-500 font-mono mt-1">
              Счет: {accountNumber} • Токен: {clientToken.substring(0, 18)}...
            </p>
          </div>
        </div>

        {/* Спидометр риска на чистом белом фоне */}
        <div className="flex items-center space-x-3 bg-slate-50/80 p-3.5 rounded-2xl border border-slate-200/60">
          <div className="text-right">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
              Вероятность риска (PD)
            </span>
            <span className={`text-2xl font-black ${
              isHighRisk ? 'text-rose-600' : isMediumRisk ? 'text-amber-600' : 'text-emerald-600'
            }`}>
              {riskProbability}%
            </span>
          </div>
          <div className="w-12 h-12 relative flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-slate-200"
                strokeWidth="4"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className={`${isHighRisk ? 'text-rose-500' : isMediumRisk ? 'text-amber-500' : 'text-emerald-500'} transition-all duration-500`}
                strokeDasharray={`${riskProbability}, 100`}
                strokeWidth="4"
                strokeLinecap="round"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <Zap className={`w-4 h-4 absolute ${isHighRisk ? 'text-rose-500' : isMediumRisk ? 'text-amber-500' : 'text-emerald-500'}`} />
          </div>
        </div>
      </div>

      {/* Центральная часть: Радар 4 осей + Ключевые финансовые параметры */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 my-6 items-center">
        
        {/* Радарная диаграмма */}
        <div className="lg:col-span-5 h-[260px] bg-slate-50/50 rounded-2xl border border-slate-100 p-2 flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
              <PolarGrid stroke="#cbd5e1" strokeDasharray="3 3" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#334155', fontSize: 11, fontWeight: 600 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94a3b8" tick={false} />
              <Radar
                name="Профиль заемщика"
                dataKey="value"
                stroke={isHighRisk ? '#e11d48' : isMediumRisk ? '#d97706' : '#059669'}
                fill={isHighRisk ? '#fecdd3' : isMediumRisk ? '#fef3c7' : '#a7f3d0'}
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Финансовый статус и кнопки действий */}
        <div className="lg:col-span-7 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/70">
              <span className="text-xs text-slate-500 font-medium block">Остаток основного долга</span>
              <span className="text-xl font-extrabold text-slate-900 mt-0.5 block">
                ₸ {Math.round(currentPrincipal).toLocaleString('ru-RU')}
              </span>
            </div>
            <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200/60">
              <span className="text-xs text-emerald-800 font-medium block">Ежемесячный платеж</span>
              <span className="text-xl font-extrabold text-emerald-950 mt-0.5 block">
                ₸ {Math.round(monthlyPayment).toLocaleString('ru-RU')}
              </span>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/70 text-xs text-slate-700 leading-relaxed">
            <p className="font-semibold text-slate-900 mb-1">
              {isHighRisk
                ? '⚠️ Обнаружен высокий риск кассового разрыва'
                : '✅ Заемщик эталонно стабилен (Home Credit 360°)'}
            </p>
            {isHighRisk
              ? 'Нейросеть выявила деградацию ликвидной подушки. Рекомендуется активировать оптимизатор OR-Tools для формирования 3 щадящих планов с продлением срока.'
              : 'Показатели полного 360° аудита: DTI 12.1%, опережение графика погашения на 5.4 дня, 0 отказов банков, 0 задолженностей в сторонних банках ПКБ.'}
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={onEvaluate}
              disabled={isEvaluating}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition-all flex items-center space-x-2 active:scale-95 disabled:opacity-50 cursor-pointer"
            >
              <Sparkles className="w-4 h-4" />
              <span>Подобрать план ИИ (OR-Tools)</span>
            </button>

            {onOpenHistory && (
              <button
                onClick={onOpenHistory}
                className="px-4 py-2.5 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-bold text-xs border border-emerald-300 transition-all flex items-center space-x-1.5 cursor-pointer shadow-2xs"
              >
                <History className="w-4 h-4 text-emerald-700" />
                <span>Вся история и аудит</span>
              </button>
            )}

            <button
              onClick={onOpenAgentWorld}
              className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-xs border border-slate-200 transition-all flex items-center space-x-1.5 cursor-pointer"
            >
              <span>Смотреть жизнь ботов</span>
            </button>
          </div>
        </div>

      </div>

    </div>
  );
};
