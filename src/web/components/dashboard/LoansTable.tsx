'use client';

import React, { useState } from 'react';
import { LoanSummary } from '@/lib/api';
import { BrainCircuit, AlertTriangle, CheckCircle2, ChevronRight, RefreshCw, Search, ShieldCheck, History } from 'lucide-react';

interface LoansTableProps {
  loans: LoanSummary[];
  isLoading: boolean;
  onEvaluate: (loanId: string) => void;
  isEvaluating: boolean;
  onSelectLoan: (loanId: string) => void;
  onOpenHistory?: (loan: LoanSummary) => void;
}

export const LoansTable: React.FC<LoansTableProps> = ({
  loans,
  isLoading,
  onEvaluate,
  isEvaluating,
  onSelectLoan,
  onOpenHistory,
}) => {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'risk' | 'stable'>('all');

  const filteredLoans = loans.filter((loan) => {
    const matchesSearch =
      loan.accountNumber.toLowerCase().includes(search.toLowerCase()) ||
      loan.clientToken.toLowerCase().includes(search.toLowerCase());

    const riskProb = loan.lastScoring ? Math.round(loan.lastScoring.pDefault30d * 100) : 15;
    const isRisk = riskProb > 40;

    if (filter === 'risk') return matchesSearch && isRisk;
    if (filter === 'stable') return matchesSearch && !isRisk;
    return matchesSearch;
  });

  if (isLoading) {
    return (
      <div className="glass-card rounded-2xl p-12 text-center text-slate-500">
        <RefreshCw className="w-8 h-8 animate-spin mx-auto text-emerald-600 mb-3" />
        <p className="font-medium">Загрузка данных кредитного портфеля...</p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl overflow-hidden border border-emerald-500/20 bg-white/95 shadow-sm">
      
      {/* Панель управления с поиском и фильтрами */}
      <div className="p-6 border-b border-emerald-500/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-800 flex items-center space-x-2">
            <span>Мониторинг заемщиков в реальном времени</span>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-100/80 px-2.5 py-0.5 rounded-full">
              {filteredLoans.length} из {loans.length} клиентов
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Искусственный интеллект непрерывно отслеживает риски до наступления дефолта
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Поиск по номеру счета..."
              className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50/50"
            />
          </div>

          <div className="flex items-center space-x-1 p-1 bg-slate-100/80 rounded-xl text-xs">
            <button
              onClick={() => setFilter('all')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'all' ? 'bg-white text-slate-800 shadow-xs' : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              Все
            </button>
            <button
              onClick={() => setFilter('risk')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'risk' ? 'bg-amber-100 text-amber-900 shadow-xs font-semibold' : 'text-slate-500 hover:text-amber-800'
              }`}
            >
              В зоне риска
            </button>
            <button
              onClick={() => setFilter('stable')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'stable' ? 'bg-emerald-100 text-emerald-900 shadow-xs font-semibold' : 'text-slate-500 hover:text-emerald-800'
              }`}
            >
              Стабильные
            </button>
          </div>
        </div>
      </div>

      {/* Таблица */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-emerald-50/50 text-emerald-950 text-xs font-semibold uppercase tracking-wider border-b border-emerald-500/10">
              <th className="py-3.5 px-6">Заемщик</th>
              <th className="py-3.5 px-6">Остаток долга</th>
              <th className="py-3.5 px-6">Ежемесячный платеж</th>
              <th className="py-3.5 px-6">Оценка риска (ИИ)</th>
              <th className="py-3.5 px-6">Статус поведения</th>
              <th className="py-3.5 px-6 text-right">Действие</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-emerald-500/10 text-sm">
            {filteredLoans.map((loan) => {
              const riskProb = loan.lastScoring ? Math.round(loan.lastScoring.pDefault30d * 100) : 15;
              const isHighRisk = riskProb > 40;

              return (
                <tr
                  key={loan.loanId}
                  className="hover:bg-emerald-50/40 transition-colors duration-150 cursor-pointer"
                  onClick={() => onSelectLoan(loan.loanId)}
                >
                  <td className="py-4 px-6">
                    <div className="font-semibold text-slate-800">
                      Счет: {loan.accountNumber}
                    </div>
                    <div className="text-xs text-slate-400 font-mono">
                      ID: {loan.clientToken.substring(0, 13)}...
                    </div>
                  </td>

                  <td className="py-4 px-6 font-semibold text-slate-700">
                    ₸ {Math.round(loan.currentPrincipalBalance).toLocaleString('ru-RU')}
                  </td>

                  <td className="py-4 px-6 text-slate-600">
                    ₸ {Math.round(loan.monthlyPayment).toLocaleString('ru-RU')}
                  </td>

                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-slate-100 rounded-full h-2.5 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            isHighRisk
                              ? riskProb > 75
                                ? 'bg-rose-500'
                                : 'bg-amber-500'
                              : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(riskProb, 100)}%` }}
                        />
                      </div>
                      <span
                        className={`text-xs font-bold ${
                          isHighRisk
                            ? riskProb > 75
                              ? 'text-rose-600'
                              : 'text-amber-600'
                            : 'text-emerald-700'
                        }`}
                      >
                        {riskProb}%
                      </span>
                    </div>
                  </td>

                  <td className="py-4 px-6">
                    {isHighRisk ? (
                      <span className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${
                        riskProb > 75
                          ? 'bg-rose-100/80 text-rose-800 border-rose-300/40'
                          : 'bg-amber-100/80 text-amber-800 border-amber-300/40'
                      }`}>
                        <AlertTriangle className={`w-3.5 h-3.5 ${riskProb > 75 ? 'text-rose-600' : 'text-amber-600'}`} />
                        <span>{riskProb > 75 ? 'Критический риск' : 'Ранний сигнал'}</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100/80 text-emerald-800 border border-emerald-300/40">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Стабилен</span>
                      </span>
                    )}
                  </td>

                  <td className="py-4 px-6 text-right" onClick={(e) => e.stopPropagation()}>
                    <div className="flex items-center justify-end space-x-2">
                      {onOpenHistory && (
                        <button
                          onClick={() => onOpenHistory(loan)}
                          className="inline-flex items-center space-x-1 px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-emerald-50 text-slate-700 hover:text-emerald-800 border border-slate-200 hover:border-emerald-300 transition-all shadow-2xs"
                          title="Посмотреть историю изменений и влияние на риск"
                        >
                          <History className="w-3.5 h-3.5 text-emerald-600" />
                          <span>История</span>
                        </button>
                      )}
                      <button
                        onClick={() => onEvaluate(loan.loanId)}
                        disabled={isEvaluating}
                        className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white shadow-sm transition-all duration-200 active:scale-95 disabled:opacity-50"
                      >
                        <BrainCircuit className="w-3.5 h-3.5" />
                        <span>Подобрать план ИИ</span>
                        <ChevronRight className="w-3.5 h-3.5 opacity-70" />
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};