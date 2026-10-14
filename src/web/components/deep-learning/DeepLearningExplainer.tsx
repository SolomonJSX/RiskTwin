'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Eye, Network } from 'lucide-react';

export interface AttentionToken {
  day: string;
  event: string;
  weight: number; // 0.0 - 1.0 (Attention weight alpha)
  category: 'income' | 'spend' | 'microloan' | 'night_activity';
}

interface DeepLearningExplainerProps {
  clientName: string;
  accountNumber: string;
  tokens: AttentionToken[];
}

export const DeepLearningExplainer: React.FC<DeepLearningExplainerProps> = ({
  clientName,
  accountNumber,
  tokens,
}) => {
  return (
    <div className="rounded-3xl p-6 bg-slate-900/90 border border-emerald-500/30 shadow-2xl backdrop-blur-xl space-y-6">
      
      {/* Шапка модуля Deep Learning */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-emerald-500/20 gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-300 flex items-center justify-center text-slate-950 font-bold shadow-lg shadow-emerald-500/30">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-white tracking-wide">
                Архитектура Deep Learning • Вектор внимания: {clientName}
              </h3>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Cross-Attention 4 Heads
              </span>
            </div>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Счет: {accountNumber} • Временной анализ скрытой траектории риска
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400 bg-emerald-950/60 px-3 py-1.5 rounded-xl border border-emerald-500/20">
          <Eye className="w-4 h-4 text-emerald-400" />
          <span>Скрытый размер эмбеддинга: d=128</span>
        </div>
      </div>

      {/* Интерактивная карта внимания (Attention Weights) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-300">
          <span className="font-semibold flex items-center space-x-2">
            <Network className="w-4 h-4 text-emerald-400" />
            <span>Тепловая карта внимания нейросети (На что модель обратила внимание):</span>
          </span>
          <span className="text-[11px] text-slate-400 font-mono">Вес важности (Attention Score α)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <AnimatePresence mode="popLayout">
            {tokens.map((t, idx) => (
              <motion.div
                key={`${t.day}-${t.event}-${idx}`}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.25, delay: idx * 0.05 }}
                className={`p-3.5 rounded-2xl border transition-all duration-300 ${
                  t.weight > 0.8
                    ? 'bg-rose-950/30 border-rose-500/40 hover:border-rose-400 shadow-lg shadow-rose-950/30'
                    : t.weight > 0.4
                    ? 'bg-amber-950/30 border-amber-500/30 hover:border-amber-400'
                    : 'bg-slate-800/40 border-slate-700/50 hover:border-emerald-500/30'
                }`}
              >
                <div className="flex items-center justify-between text-xs mb-1.5">
                  <span className="font-mono text-slate-400 text-[11px]">{t.day}</span>
                  <span className={`font-mono font-bold text-xs ${
                    t.weight > 0.8 ? 'text-rose-400' : t.weight > 0.4 ? 'text-amber-400' : 'text-emerald-400'
                  }`}>
                    α = {(t.weight).toFixed(2)}
                  </span>
                </div>

                <div className="text-xs font-medium text-slate-200 line-clamp-2 mb-2 min-h-[32px]">
                  {t.event}
                </div>

                {/* Полоска веса внимания */}
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      t.weight > 0.8
                        ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                        : t.weight > 0.4
                        ? 'bg-gradient-to-r from-emerald-500 to-amber-500'
                        : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.min(t.weight * 100, 100)}%` }}
                  />
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Сравнение: Традиционный скоринг vs RiskTwin Deep Learning */}
      <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-950 via-emerald-950/40 to-slate-950 border border-emerald-500/20 text-xs">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-rose-400 uppercase tracking-wider block">
              ❌ Классический скоринг банка (без Deep Learning):
            </span>
            <p className="text-slate-300">
              Видит только баланс счета. Узнает о проблеме лишь на <strong>30-й день фактической просрочки</strong>, когда кредит уже сорван и банк теряет капитал.
            </p>
          </div>

          <div className="space-y-1 md:border-l md:border-slate-800 md:pl-4">
            <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider block">
              ✅ RiskTwin Deep Learning (Вектор внимания):
            </span>
            <p className="text-slate-200">
              Выявляет эмоциональный и кассовый стресс по последовательности транзакций <strong>за 45 дней ДО первой просрочки</strong> и спасает заемщика без штрафов.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};
