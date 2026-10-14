'use client';

import React, { useState } from 'react';
import { LoanSummary } from '@/lib/api';
import { BrainCircuit, AlertTriangle, CheckCircle2, ChevronRight, RefreshCw, Search, History } from 'lucide-react';

interface LoansTableProps {
  loans: LoanSummary[];
  isLoading: boolean;
  onEvaluate: (loanId: string) => void;
  isEvaluating: boolean;
  onSelectLoan: (loanId: string) => void;
  selectedLoanId?: string | null;
  onOpenHistory?: (accountNumber: string) => void;
}

const BOT_PROFILES: Record<string, { name: string; role: string; avatar: string }> = {
  'KZ886010002003004001': { name: 'Арман', role: 'IT-Сеньор', avatar: '👨‍💻' },
  'KZ886010002003004002': { name: 'Жанна', role: 'Маркетолог / SMM', avatar: '👩‍💼' },
  'KZ886010002003004003': { name: 'Санжар', role: 'Инженер на производстве', avatar: '👷‍♂️' },
};

export const LoansTable: React.FC<LoansTableProps> = ({
  loans,
  isLoading,
  onEvaluate,
  isEvaluating,
  onSelectLoan,
  selectedLoanId,
  onOpenHistory,
}) => {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<'all' | 'risk' | 'stable'>('all');

  const filteredLoans = loans.filter((loan) => {
    const profile = BOT_PROFILES[loan.accountNumber] || { name: 'Арман', role: 'IT-Сеньор' };
    const matchesSearch =
      profile.name.toLowerCase().includes(search.toLowerCase()) ||
      profile.role.toLowerCase().includes(search.toLowerCase()) ||
      loan.accountNumber.toLowerCase().includes(search.toLowerCase());

    const riskProb = loan.lastScoring ? Math.round(loan.lastScoring.pDefault30d * 100) : 1;
    const isRisk = riskProb > 40;

    if (filter === 'risk') return matchesSearch && isRisk;
    if (filter === 'stable') return matchesSearch && !isRisk;
    return matchesSearch;
  });

  if (isLoading) {
    return (
      <div className="glass-card rounded-2xl p-12 text-center text-slate-500">
        <RefreshCw className="w-8 h-8 animate-spin mx-auto text-emerald-600 mb-3" />
        <p className="font-medium">Загрузка данных портфеля...</p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-3xl overflow-hidden border border-slate-200/80 bg-white shadow-sm w-full">
      
      {/* Аккуратная шапка таблицы без наездов */}
      <div className="p-6 border-b border-slate-100 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-extrabold text-slate-900 flex items-center space-x-2">
            <span>Реестр цифровых двойников заемщиков</span>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
              {filteredLoans.length} активных профилей
            </span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Кликните на строку, чтобы открыть полную историю и аудит 360° цифрового двойника
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Поиск по имени или счету..."
              className="pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-slate-50 w-56"
            />
          </div>

          <div className="flex items-center space-x-1 p-1 bg-slate-100 rounded-xl text-xs">
            <button
              onClick={() => setFilter('all')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'all' ? 'bg-white text-slate-900 shadow-xs font-bold' : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              Все ({filteredLoans.length})
            </button>
            <button
              onClick={() => setFilter('risk')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'risk' ? 'bg-white text-amber-900 shadow-xs font-bold' : 'text-slate-500 hover:text-amber-800'
              }`}
            >
              В зоне риска (0)
            </button>
            <button
              onClick={() => setFilter('stable')}
              className={`px-3 py-1 rounded-lg font-medium transition-all ${
                filter === 'stable' ? 'bg-white text-emerald-900 shadow-xs font-bold' : 'text-slate-500 hover:text-emerald-800'
              }`}
            >
              Стабильные ({filteredLoans.length})
            </button>
          </div>
        </div>
      </div>

      {/* Полноразмерная таблица без обрезаний */}
      <div className="w-full">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200/80">
              <th className="py-3.5 px-6">Заемщик</th>
              <th className="py-3.5 px-6">Остаток долга</th>
              <th className="py-3.5 px-6">Платеж в месяц</th>
              <th className="py-3.5 px-6">Риск дефолта (PD)</th>
              <th className="py-3.5 px-6">Статус поведения</th>
              <th className="py-3.5 px-6 text-right">Действие</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {filteredLoans.map((loan) => {
              const profile = BOT_PROFILES[loan.accountNumber] || { name: 'Арман', role: 'IT-Сеньор', avatar: '👨‍💻' };
              const riskProbNum = loan.lastScoring ? loan.lastScoring.pDefault30d * 100 : 1.3;
              const riskProbStr = riskProbNum.toFixed(1);
              const isHighRisk = riskProbNum > 50;
              const isMediumRisk = riskProbNum > 25 && riskProbNum <= 50;
              const isSelected = selectedLoanId === loan.loanId;

              return (
                <tr
                  key={loan.loanId}
                  className={`transition-colors duration-150 cursor-pointer ${
                    isSelected ? 'bg-emerald-50/80 border-l-4 border-emerald-600' : 'hover:bg-slate-50/60'
                  }`}
                  onClick={() => onSelectLoan(loan.loanId)}
                >
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">{profile.avatar}</span>
                      <div>
                        <div className="font-extrabold text-slate-900 flex items-center space-x-1.5">
                          <span>{profile.name}</span>
                          <span className="text-xs font-normal text-slate-500">({profile.role})</span>
                          {loan.accountNumber === 'KZ886010002003004001' && (
                            <span className="text-[10px] font-bold px-1.5 py-0.2 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">
                              360° Эталон
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-slate-500 font-mono mt-0.5">
                          {loan.accountNumber}
                        </div>
                      </div>
                    </div>
                  </td>

                  <td className="py-4 px-6 font-bold text-slate-800">
                    ₸ {Math.round(loan.currentPrincipalBalance).toLocaleString('ru-RU')}
                  </td>

                  <td className="py-4 px-6 text-slate-600 font-medium">
                    ₸ {Math.round(loan.monthlyPayment).toLocaleString('ru-RU')}
                  </td>

                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-2.5">
                      <div className="w-24 bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            isHighRisk
                              ? 'bg-rose-500'
                              : isMediumRisk
                              ? 'bg-amber-500'
                              : 'bg-emerald-500'
                          }`}
                          style={{ width: `${Math.min(riskProbNum, 100)}%` }}
                        />
                      </div>
                      <span
                        className={`text-xs font-black font-mono ${
                          isHighRisk
                            ? 'text-rose-600'
                            : isMediumRisk
                            ? 'text-amber-600'
                            : 'text-emerald-600'
                        }`}
                      >
                        {riskProbStr}%
                      </span>
                    </div>
                  </td>

                  <td className="py-4 px-6">
                    {isHighRisk ? (
                      <span className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
                        <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                        <span>Критический риск</span>
                      </span>
                    ) : isMediumRisk ? (
                      <span className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                        <span>Ранний сигнал</span>
                      </span>
                    ) : (
                      <span className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        <span>Стабилен</span>
                      </span>
                    )}
                  </td>

                  <td className="py-4 px-6 text-right" onClick={(e) => e.stopPropagation()}>
                    <div className="flex items-center justify-end space-x-2">
                      {onOpenHistory && (
                        <button
                          onClick={() => {
                            onSelectLoan(loan.loanId);
                            onOpenHistory(loan.accountNumber);
                          }}
                          title="Посмотреть всю историю бота"
                          className="p-2 rounded-xl text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 border border-slate-200 transition-all cursor-pointer shadow-2xs"
                        >
                          <History className="w-3.5 h-3.5" />
                        </button>
                      )}
                      <button
                        onClick={() => onEvaluate(loan.loanId)}
                        disabled={isEvaluating}
                        className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition-all active:scale-95 disabled:opacity-50 whitespace-nowrap cursor-pointer"
                      >
                        <BrainCircuit className="w-3.5 h-3.5" />
                        <span>План ИИ</span>
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