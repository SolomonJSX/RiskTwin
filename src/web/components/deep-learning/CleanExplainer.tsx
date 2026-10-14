'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Eye, Network, CheckCircle2, History } from 'lucide-react';
import { AttentionToken } from './DeepLearningExplainer';

interface CleanExplainerProps {
  clientName: string;
  accountNumber: string;
  tokens: AttentionToken[];
  onOpenHistory?: () => void;
}

export const CleanExplainer: React.FC<CleanExplainerProps> = ({
  clientName,
  accountNumber,
  tokens,
  onOpenHistory,
}) => {
  return (
    <div className="glass-card rounded-3xl p-6 bg-white border border-slate-200/80 shadow-md space-y-5">
      
      {/* Шапка */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 gap-3">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-slate-900 tracking-tight">
                Архитектура Deep Learning • Вектор внимания: {clientName}
              </h3>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
                PyTorch Cross-Attention
              </span>
            </div>
            <p className="text-xs text-slate-500 font-mono mt-0.5">
              Счет: {accountNumber} • Поведенческий анализ транзакций во времени
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2.5">
          {onOpenHistory && (
            <button
              onClick={onOpenHistory}
              className="flex items-center space-x-1.5 text-xs font-bold text-emerald-800 bg-emerald-50 hover:bg-emerald-100 px-3.5 py-1.5 rounded-xl border border-emerald-300 transition-all cursor-pointer shadow-2xs"
            >
              <History className="w-3.5 h-3.5 text-emerald-600" />
              <span>Вся история бота</span>
            </button>
          )}
          <div className="flex items-center space-x-2 text-xs text-slate-600 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <Eye className="w-4 h-4 text-emerald-600" />
            <span>Размер эмбеддинга: d=128</span>
          </div>
        </div>
      </div>

      {/* Интерактивная карта внимания */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-600">
          <span className="font-semibold flex items-center space-x-2">
            <Network className="w-4 h-4 text-emerald-600" />
            <span>Тепловая карта внимания нейросети (На что модель обратила внимание):</span>
          </span>
          <span className="text-[11px] text-slate-400 font-mono">Вес важности (Score α)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <AnimatePresence mode="popLayout">
            {tokens.map((t, idx) => {
              const isHigh = t.weight > 0.8;
              const isMedium = t.weight > 0.4 && t.weight <= 0.8;

              return (
                <motion.div
                  key={`${t.day}-${t.event}-${idx}`}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2, delay: idx * 0.04 }}
                  className={`p-3.5 rounded-2xl border transition-all ${
                    isHigh
                      ? 'bg-rose-50/60 border-rose-200 text-rose-950'
                      : isMedium
                      ? 'bg-amber-50/60 border-amber-200 text-amber-950'
                      : 'bg-emerald-50/40 border-emerald-100 text-emerald-950'
                  }`}
                >
                  <div className="flex items-center justify-between text-xs mb-1.5">
                    <span className="font-mono text-slate-500 text-[11px]">{t.day}</span>
                    <span className={`font-mono font-bold text-xs ${
                      isHigh ? 'text-rose-600' : isMedium ? 'text-amber-600' : 'text-emerald-700'
                    }`}>
                      α = {(t.weight).toFixed(2)}
                    </span>
                  </div>

                  <div className="text-xs font-semibold text-slate-800 line-clamp-2 mb-2 min-h-[32px]">
                    {t.event}
                  </div>

                  <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        isHigh ? 'bg-rose-500' : isMedium ? 'bg-amber-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${Math.min(t.weight * 100, 100)}%` }}
                    />
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      </div>

      {/* Понятное объяснение для любого жюри */}
      <div className="p-4 rounded-2xl bg-emerald-50/50 border border-emerald-200/60 text-xs">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <span className="text-[11px] font-bold text-rose-700 uppercase tracking-wider block">
              ❌ Классический скоринг банка:
            </span>
            <p className="text-slate-600">
              Видит только баланс. Узнает о проблеме лишь на <strong>30-й день фактической просрочки</strong>, когда кредит уже сорван и банк несет убытки.
            </p>
          </div>

          <div className="space-y-1 md:border-l md:border-emerald-200 md:pl-4">
            <span className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider block">
              ✅ RiskTwin Deep Learning:
            </span>
            <p className="text-slate-700">
              Выявляет стресс по цепочке микро-транзакций <strong>за 45 дней ДО первой просрочки</strong> и предлагает клиенту помощь без штрафов.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
};
