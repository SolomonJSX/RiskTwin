'use client';

import React, { useState } from 'react';
import { Header } from '@/components/layout/Header';
import { PortfolioSummary } from '@/components/dashboard/PortfolioSummary';
import { LoansTable } from '@/components/dashboard/LoansTable';
import { StressSimulator } from '@/components/stalker/StressSimulator';
import { ClientOffersView } from '@/components/client-portal/ClientOffersView';
import { ClientHistoryModal } from '@/components/dashboard/ClientHistoryModal';
import { useRiskTwin } from '@/hooks/useRiskTwin';
import { LoanSummary } from '@/lib/api';

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<'radar' | 'simulator' | 'client-offers'>('radar');
  const [selectedLoanId, setSelectedLoanId] = useState<string | null>(null);
  const [historyLoan, setHistoryLoan] = useState<LoanSummary | null>(null);

  const {
    loansQuery,
    evaluateMutation,
    simulateStressMutation,
    signOfferMutation,
  } = useRiskTwin();

  const loans = loansQuery.data || [];
  const atRiskCount = loans.filter((l) => (l.lastScoring?.pDefault30d || 0) > 0.4).length;

  const handleEvaluate = async (loanId: string) => {
    setSelectedLoanId(loanId);
    await evaluateMutation.mutateAsync({ loanId });
    setActiveTab('client-offers');
  };

  const handleSimulate = async (payload: any) => {
    return await simulateStressMutation.mutateAsync(payload);
  };

  const handleGoToOffers = (loanId: string) => {
    setSelectedLoanId(loanId);
    setActiveTab('client-offers');
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Шапка с градиентом */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Основной контент */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Вкладка 1: Радар наблюдения */}
        {activeTab === 'radar' && (
          <div className="space-y-6">
            <PortfolioSummary
              totalCount={loans.length}
              atRiskCount={atRiskCount}
              earlyWarningsCount={Math.max(atRiskCount, 1)}
            />

            <LoansTable
              loans={loans}
              isLoading={loansQuery.isLoading}
              isEvaluating={evaluateMutation.isPending}
              onEvaluate={handleEvaluate}
              onSelectLoan={(id) => {
                setSelectedLoanId(id);
                setActiveTab('client-offers');
              }}
              onOpenHistory={(loan) => setHistoryLoan(loan)}
            />
          </div>
        )}

        {/* Модальное окно истории заемщика и влияния на риск */}
        {historyLoan && (
          <ClientHistoryModal
            clientToken={historyLoan.clientToken}
            accountNumber={historyLoan.accountNumber}
            currentRiskProb={historyLoan.lastScoring ? Math.round(historyLoan.lastScoring.pDefault30d * 100) : 15}
            lastScoring={historyLoan.lastScoring}
            onClose={() => setHistoryLoan(null)}
            onEvaluate={() => handleEvaluate(historyLoan.loanId)}
          />
        )}

        {/* Вкладка 2: Стресс-моделирование */}
        {activeTab === 'simulator' && (
          <StressSimulator
            onSimulate={handleSimulate}
            isSimulating={simulateStressMutation.isPending}
            onGoToOffers={handleGoToOffers}
          />
        )}

        {/* Вкладка 3: Витрина решений */}
        {activeTab === 'client-offers' && (
          <ClientOffersView
            loanId={selectedLoanId}
            onSignOffer={async (offerId, otpCode) => {
              return await signOfferMutation.mutateAsync({ offerId, otpCode });
            }}
          />
        )}
      </main>

      {/* Лаконичный Enterprise-подвал */}
      <footer className="border-t border-emerald-950/10 py-6 text-center text-xs text-slate-500">
        <p>RiskTwin © 2026 • Интеллектуальный двойник кредитного риска и превентивной реструктуризации</p>
      </footer>
    </div>
  );
}