'use client';

import React from 'react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Brain, Sparkles, AlertCircle, TrendingUp, ShieldCheck, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

interface TwinMetrics {
  incomeStability: number;   // 0 - 100
  debtComfort: number;       // 0 - 100
  spendingDiscipline: number;// 0 - 100
  safetyCushion: number;     // 0 - 100
  overallStress: number;     // 0 - 100
}

interface DigitalTwinCardProps {
  clientName: string;
  accountNumber: string;
  metrics: TwinMetrics;
  aiExplanation: string[];
  recommendation: string;
  onSimulateChange?: (metric: string, value: number) => void;
}

export const DigitalTwinCard: React.FC<DigitalTwinCardProps> = ({
  clientName,
  accountNumber,
  metrics,
  aiExplanation,
  recommendation,
}) => {
  const radarData = [
    { subject: 'Стабильность дохода', value: metrics.incomeStability, fullMark: 100 },
    { subject: 'Комфорт нагрузки', value: metrics.debtComfort, fullMark: 100 },
    { subject: 'Дисциплина трат', value: metrics.spendingDiscipline, fullMark: 100 },
    { subject: 'Подушка безопасности', value: metrics.safetyCushion, fullMark: 100 },
  ];

  const isHighRisk = metrics.overallStress > 60;
  const isMediumRisk = metrics.overallStress > 35 && metrics.overallStress <= 60;

  return (
    <div className="glass-card rounded-3xl p-6 bg-gradient-to-br from-white via-emerald-50/20 to-teal-50/30 border border-emerald-500/20 shadow-xl overflow-hidden relative">
      
      {/* Декоративное неоновое свечение на фоне */}
      <div className="absolute -top-24 -right-24 w-80 h-80 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -left-24 w-80 h-80 bg-teal-400/10 rounded-full blur-3xl pointer-events-none" />

      {/* Верхний статус-бар двойника */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-emerald-500/10 gap-4">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-700 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20">
              <Brain className="w-7 h-7" />
            </div>
            <span className="absolute -bottom-1 -right-1 flex h-4 w-4">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4 w-4 bg-emerald-500 border-2 border-white"></span>
            </span>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-xl font-extrabold text-slate-800">
                Цифровой двойник: {clientName}
              </h3>
              <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                LIVE TWIN
              </span>
            </div>
            <p className="text-xs text-slate-500 font-mono mt-0.5">
              Счет: {accountNumber} • Нейросетевая проекция поведения
            </p>
          </div>
        </div>

        {/* Спидометр стресса */}
        <div className="flex items-center space-x-3 bg-white/90 p-3 rounded-2xl border border-emerald-500/20 shadow-xs">
          <div className="text-right">
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
              Индекс стресса
            </span>
            <span className={`text-2xl font-black ${
              isHighRisk ? 'text-rose-600' : isMediumRisk ? 'text-amber-600' : 'text-emerald-600'
            }`}>
              {metrics.overallStress}%
            </span>
          </div>
          <div className="w-12 h-12 relative flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-slate-100"
                strokeWidth="4"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className={`${isHighRisk ? 'text-rose-500' : isMediumRisk ? 'text-amber-500' : 'text-emerald-500'} transition-all duration-700 ease-out`}
                strokeDasharray={`${metrics.overallStress}, 100`}
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

      {/* Центральная часть: Радар поведения + Нейро-объяснение XAI */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 my-6 items-center">
        
        {/* Радарная диаграмма (Spider Radar Chart) */}
        <div className="lg:col-span-5 h-[270px] relative flex items-center justify-center bg-white/60 rounded-2xl border border-emerald-500/10 p-2">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
              <PolarGrid stroke="#a7f3d0" strokeDasharray="3 3" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: '#064e3b', fontSize: 11, fontWeight: 600 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#6ee7b7" tick={false} />
              <Radar
                name="Профиль заемщика"
                dataKey="value"
                stroke={isHighRisk ? '#f43f5e' : isMediumRisk ? '#f59e0b' : '#059669'}
                fill={isHighRisk ? '#fda4af' : isMediumRisk ? '#fde68a' : '#34d399'}
                fillOpacity={0.5}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Нейросетевое объяснение: "Почему ИИ так думает" */}
        <div className="lg:col-span-7 space-y-3">
          <div className="flex items-center space-x-2 text-xs font-bold text-emerald-950 uppercase tracking-wider">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Нейросетевой разбор поведения (Explainable AI)</span>
          </div>

          <div className="space-y-2">
            {aiExplanation.map((fact, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="p-3 rounded-xl bg-white/90 border border-emerald-500/15 shadow-xs flex items-start space-x-3 text-xs"
              >
                <div className="p-1 rounded-md bg-emerald-100 text-emerald-700 flex-shrink-0 mt-0.5">
                  <TrendingUp className="w-3.5 h-3.5" />
                </div>
                <div className="text-slate-700 font-medium leading-relaxed">
                  {fact}
                </div>
              </motion.div>
            ))}
          </div>

          {/* Резюме ИИ и предиктивный вывод */}
          <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-900 to-teal-900 text-white shadow-md text-xs mt-3">
            <div className="flex items-center space-x-2 font-bold text-emerald-300 mb-1">
              <ShieldCheck className="w-4 h-4" />
              <span>Решение предиктивного ядра:</span>
            </div>
            <p className="text-emerald-100/95 leading-relaxed">
              {recommendation}
            </p>
          </div>
        </div>

      </div>

    </div>
  );
};
