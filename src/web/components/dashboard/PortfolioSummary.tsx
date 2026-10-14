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
      
      {/* Карточка 1: Индекс устойчивости (Зеленый градиент + Белый контрастный текст) */}
      <div className="rounded-2xl p-5 bg-gradient-to-br from-emerald-600 via-emerald-700 to-teal-800 text-white shadow-md">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold tracking-wider uppercase text-emerald-100">
            Индекс устойчивости
          </span>
          <div className="p-2 rounded-xl bg-white/20 text-white backdrop-blur-xs">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold tracking-tight text-white">94.8%</span>
          <span className="text-xs font-semibold text-emerald-950 bg-emerald-200 px-2 py-0.5 rounded-full">
            Высокий
          </span>
        </div>
        <p className="mt-1.5 text-xs text-emerald-100/90 font-medium">
          Портфель защищен от скрытых дефолтов
        </p>
      </div>

      {/* Карточка 2: Активных клиентов */}
      <div className="rounded-2xl p-5 bg-gradient-to-br from-teal-600 via-teal-700 to-emerald-800 text-white shadow-md">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold tracking-wider uppercase text-teal-100">
            Активных клиентов
          </span>
          <div className="p-2 rounded-xl bg-white/20 text-white backdrop-blur-xs">
            <Sparkles className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold tracking-tight text-white">{totalCount}</span>
          <span className="text-xs text-teal-100 font-medium">профилей</span>
        </div>
        <p className="mt-1.5 text-xs text-teal-100/90 font-medium">
          С непрерывным цифровым мониторингом
        </p>
      </div>

      {/* Карточка 3: Ранние сигналы */}
      <div className="rounded-2xl p-5 bg-gradient-to-br from-amber-600 to-orange-700 text-white shadow-md">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold tracking-wider uppercase text-amber-100">
            Ранние сигналы
          </span>
          <div className="p-2 rounded-xl bg-white/20 text-white backdrop-blur-xs">
            <BellRing className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold tracking-tight text-white">{earlyWarningsCount}</span>
          <span className="text-xs font-semibold text-amber-950 bg-amber-200 px-2 py-0.5 rounded-full">
            До просрочки
          </span>
        </div>
        <p className="mt-1.5 text-xs text-amber-100/90 font-medium">
          Предупреждения сработали заблаговременно
        </p>
      </div>

      {/* Карточка 4: Сбережение средств */}
      <div className="rounded-2xl p-5 bg-gradient-to-br from-emerald-700 via-teal-800 to-emerald-900 text-white shadow-md">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold tracking-wider uppercase text-emerald-100">
            Сбережение средств
          </span>
          <div className="p-2 rounded-xl bg-white/20 text-white backdrop-blur-xs">
            <TrendingDown className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-3 flex items-baseline space-x-2">
          <span className="text-3xl font-extrabold tracking-tight text-white">₸ 14.2M</span>
          <span className="text-xs font-semibold text-emerald-950 bg-emerald-200 px-2 py-0.5 rounded-full">
            +32% NPV
          </span>
        </div>
        <p className="mt-1.5 text-xs text-emerald-100/90 font-medium">
          Предотвращение судебных и резервных потерь
        </p>
      </div>

    </div>
  );
};