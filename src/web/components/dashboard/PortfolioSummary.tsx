'use client';

import React from 'react';
import { ShieldCheck, TrendingDown, BellRing, Sparkles } from 'lucide-react';

interface SummaryProps {
  totalCount: number;
  atRiskCount: number;
  earlyWarningsCount: number;
}

export const PortfolioSummary: React.FC<SummaryProps> = ({
  totalCount,
  atRiskCount,
  earlyWarningsCount,
}) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      
      {/* Карточка 1: Здоровье портфеля */}
      <div className="glass-card glass-card-hover rounded-2xl p-5 border border-emerald-500/20 bg-white/80">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold tracking-wider uppercase text-emerald-800">
            Индекс устойчивости
          </span>
          <div className="p-2 rounded-xl bg-emerald-100/80 text-emerald-700">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-bold tracking-tight text-slate-800">94.8%</span>
          <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
            Высокий
          </span>
        </div>
        <p className="mt-1.5 text-xs text-slate-500">
          Портфель защищен от скрытых дефолтов
        </p>
      </div>

      {/* Карточка 2: Заемщиков под защитой */}
      <div className="glass-card glass-card-hover rounded-2xl p-5 border border-emerald-500/20 bg-white/80">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold tracking-wider uppercase text-emerald-800">
            Активных клиентов
          </span>
          <div className="p-2 rounded-xl bg-emerald-100/80 text-emerald-700">
            <Sparkles className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-bold tracking-tight text-slate-800">{totalCount}</span>
          <span className="text-xs text-slate-500">профилей</span>
        </div>
        <p className="mt-1.5 text-xs text-slate-500">
          С непрерывным цифровым мониторингом
        </p>
      </div>

      {/* Карточка 3: Ранние сигналы тревоги */}
      <div className="glass-card glass-card-hover rounded-2xl p-5 border border-emerald-500/20 bg-white/80">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold tracking-wider uppercase text-amber-800">
            Ранние сигналы
          </span>
          <div className="p-2 rounded-xl bg-amber-100/80 text-amber-700">
            <BellRing className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-bold tracking-tight text-amber-600">{earlyWarningsCount}</span>
          <span className="text-xs font-medium text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
            До просрочки
          </span>
        </div>
        <p className="mt-1.5 text-xs text-slate-500">
          Предупреждения сработали заблаговременно
        </p>
      </div>

      {/* Карточка 4: Спасенный капитал */}
      <div className="glass-card glass-card-hover rounded-2xl p-5 border border-emerald-500/20 bg-white/80">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold tracking-wider uppercase text-emerald-800">
            Сбережение средств
          </span>
          <div className="p-2 rounded-xl bg-teal-100/80 text-teal-700">
            <TrendingDown className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-bold tracking-tight text-slate-800">₸ 14.2M</span>
          <span className="text-xs font-medium text-teal-700 bg-teal-50 px-2 py-0.5 rounded-full border border-teal-200">
            +32% NPV
          </span>
        </div>
        <p className="mt-1.5 text-xs text-slate-500">
          Предотвращение судебных и резервных потерь
        </p>
      </div>

    </div>
  );
};