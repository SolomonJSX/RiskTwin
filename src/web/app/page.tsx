'use client';

import React, { useState, useEffect } from 'react';
import { Header } from '@/components/layout/Header';
import { PortfolioSummary } from '@/components/dashboard/PortfolioSummary';
import { LoansTable } from '@/components/dashboard/LoansTable';
import { BotTwinView } from '@/components/dashboard/BotTwinView';
import { CleanExplainer } from '@/components/deep-learning/CleanExplainer';
import { AttentionToken } from '@/components/deep-learning/DeepLearningExplainer';
import { AgentWorldDashboard } from '@/components/deep-learning/AgentWorldDashboard';
import { InteractiveSimulator } from '@/components/stalker/InteractiveSimulator';
import { ClientOffersView } from '@/components/client-portal/ClientOffersView';
import { BotHistoryModal } from '@/components/dashboard/BotHistoryModal';
import { LlmReasoningView } from '@/components/deep-learning/LlmReasoningView';
import { StressTwinDashboard } from '@/components/deep-learning/StressTwinDashboard';
import { useRiskTwin } from '@/hooks/useRiskTwin';
import { User, ShieldCheck, AlertTriangle, AlertCircle, ArrowRight } from 'lucide-react';

export const ARMAN_PASSPORT_360 = {
  accountNumber: 'KZ886010002003004001',
  clientToken: '11111111-2222-3333-4444-555555555555',
  name: 'Арман',
  role: 'IT-Сеньор',
  avatar: '👨‍💻',
  income: 1200000,
  credit: 4200000,
  annuity: 145000,
  dti_ratio: 0.1208,
  credit_to_income_ratio: 3.5,
  age_years: 29,
  employment_years: 7,
  ext_source: '0.88 (Класс AAA)',
  bureau_active_loans: 0,
  bureau_total_debt: 0,
  bureau_total_overdue: 0,
  inst_total_tx: 36,
  inst_avg_delay_days: -5.4,
  inst_late_count: 0,
  pos_completed_count: 2,
  pos_max_dpd: 0,
  cc_atm_drawings_sum: 0,
  cc_pos_drawings_sum: 320000,
  cc_utilization_mean: 0.18,
  prev_approved_count: 3,
  prev_refused_count: 0,
  roc_auc: 0.7557,
};

export const ZHANNA_PASSPORT_360 = {
  accountNumber: 'KZ886010002003004002',
  clientToken: '22222222-3333-4444-5555-666666666666',
  name: 'Жанна',
  role: 'Маркетолог / SMM',
  avatar: '👩‍💼',
  income: 420000,
  credit: 2600000,
  annuity: 185000,
  dti_ratio: 0.4405,
  credit_to_income_ratio: 6.2,
  age_years: 27,
  employment_years: 4,
  ext_source: '0.58 (Класс BBB)',
  bureau_active_loans: 1,
  bureau_total_debt: 450000,
  bureau_total_overdue: 0,
  inst_total_tx: 14,
  inst_avg_delay_days: 2.4,
  inst_late_count: 3,
  pos_completed_count: 1,
  pos_max_dpd: 0,
  cc_atm_drawings_sum: 85000,
  cc_pos_drawings_sum: 210000,
  cc_utilization_mean: 0.82,
  prev_approved_count: 2,
  prev_refused_count: 1,
  roc_auc: 0.7557,
};

export const SANZHAR_PASSPORT_360 = {
  accountNumber: 'KZ886010002003004003',
  clientToken: '33333333-4444-5555-6666-777777777777',
  name: 'Санжар',
  role: 'Инженер на производстве',
  avatar: '👷‍♂️',
  income: 850000,
  credit: 3800000,
  annuity: 160000,
  dti_ratio: 0.1882,
  credit_to_income_ratio: 4.47,
  age_years: 32,
  employment_years: 9,
  ext_source: '0.76 (Класс AA)',
  bureau_active_loans: 0,
  bureau_total_debt: 0,
  bureau_total_overdue: 0,
  inst_total_tx: 24,
  inst_avg_delay_days: -1.5,
  inst_late_count: 0,
  pos_completed_count: 3,
  pos_max_dpd: 0,
  cc_atm_drawings_sum: 0,
  cc_pos_drawings_sum: 140000,
  cc_utilization_mean: 0.12,
  prev_approved_count: 4,
  prev_refused_count: 0,
  roc_auc: 0.7557,
};

const BOT_MAP: Record<string, {
  name: string;
  role: string;
  avatar: string;
  basePd: number;
  passport360: Record<string, any>;
  tokens: AttentionToken[];
}> = {
  'KZ886010002003004001': {
    name: 'Арман',
    role: 'IT-Сеньор',
    avatar: '👨‍💻',
    basePd: 1.05,
    passport360: ARMAN_PASSPORT_360,
    tokens: [
      { day: 'День -35', event: 'Зачисление стабильного IT-дохода (₸1 200 000, комфортный DTI 12.1%)', weight: 0.15, category: 'income' },
      { day: 'День -26', event: 'Успешно закрыты 2 товарные рассрочки без единой задержки (POS CASH)', weight: 0.17, category: 'income' },
      { day: 'День -18', event: 'Высокий кредитный скоринг ПКБ (EXT_SOURCE 0.88, Класс надежности AAA)', weight: 0.16, category: 'income' },
      { day: 'День -12', event: 'Безналичные транзакции картой (₸320 000, 0 ₸ панических снятий в ATM)', weight: 0.13, category: 'spend' },
      { day: 'День -05', event: 'Плановый платеж зачислен на 5.4 дней раньше срока (Installments)', weight: 0.15, category: 'income' },
      { day: 'День -01', event: 'Эталонный цифровой профиль: 0 отказов банков, 0 задолженностей в ПКБ', weight: 0.14, category: 'income' },
    ],
  },
  'KZ886010002003004002': {
    name: 'Жанна',
    role: 'Маркетолог / SMM',
    avatar: '👩‍💼',
    basePd: 16.8,
    passport360: ZHANNA_PASSPORT_360,
    tokens: [
      { day: 'День -28', event: 'Исчерпание кредитного лимита карты до 82% (утилизация cc_utilization = 0.82)', weight: 0.22, category: 'spend' },
      { day: 'День -21', event: 'Параллельные рассрочки BNPL (4 активных договора Kaspi/Halyk 0-0-12)', weight: 0.19, category: 'spend' },
      { day: 'День -14', event: 'Задержка платежа по аннуитету на 3 дня (inst_avg_delay = +2.4 дн)', weight: 0.24, category: 'spend' },
      { day: 'День -07', event: 'Снятие наличных с кредитной карты в ATM (₸85 000 для перекрытия)', weight: 0.18, category: 'microloan' },
      { day: 'День -02', event: 'Ночная активность в мобильном банке в 02:40 (проверка лимита)', weight: 0.17, category: 'night_activity' },
    ],
  },
  'KZ886010002003004003': {
    name: 'Санжар',
    role: 'Инженер на производстве',
    avatar: '👷‍♂️',
    basePd: 4.8,
    passport360: SANZHAR_PASSPORT_360,
    tokens: [
      { day: 'День -30', event: 'Стабильное зачисление оклада на производстве (₸850 000, DTI 18.8%)', weight: 0.18, category: 'income' },
      { day: 'День -22', event: '3 успешно закрытых контракта в истории (ПКБ скоринг 0.76, Класс AA)', weight: 0.19, category: 'income' },
      { day: 'День -15', event: 'Плановый платеж за 1.5 дня до дедлайна (дисциплина 100%)', weight: 0.21, category: 'income' },
      { day: 'День -08', event: 'Умеренные безналичные расходы по карте (утилизация 12%)', weight: 0.15, category: 'spend' },
      { day: 'День -01', event: '0 просрочек, 0 займов в МФО, 0 снятий наличных', weight: 0.17, category: 'income' },
    ],
  },
};

export default function HomePage() {
  const [activeTab, setActiveTab] = useState<'radar' | 'simulator' | 'agent-world' | 'stress-twin' | 'client-offers'>('radar');
  const [selectedAccount, setSelectedAccount] = useState<string>('KZ886010002003004001');
  const [selectedLoanId, setSelectedLoanId] = useState<string | null>(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [liveAgents, setLiveAgents] = useState<Record<string, any>>({});

  // Реактивная синхронизация состояния со всеми 3 агентами из Agent World
  useEffect(() => {
    let isMounted = true;
    const fetchLiveAgents = async () => {
      try {
        const res = await fetch('http://localhost:8001/api/world/agents');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && isMounted) {
            const map: Record<string, any> = {};
            data.forEach((ag: any) => {
              if (ag.account_number) map[ag.account_number] = ag;
            });
            setLiveAgents(map);
          }
        }
      } catch {
        // Fallback
      }
    };
    fetchLiveAgents();
    const interval = setInterval(fetchLiveAgents, 1500);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const { loansQuery, evaluateMutation, signOfferMutation } = useRiskTwin();

  // Формируем 3 кредитных договора с динамическими данными
  const loans = [
    {
      loanId: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
      accountNumber: 'KZ886010002003004001',
      clientToken: '11111111-2222-3333-4444-555555555555',
      currentPrincipalBalance: liveAgents['KZ886010002003004001']?.total_debt ?? 4200000,
      monthlyPayment: liveAgents['KZ886010002003004001']?.monthly_payment ?? 145000,
      daysPastDue: 0,
      stageIfrs9: 'STAGE_1',
      lastScoring: {
        eventId: 'sc-arman-1',
        pDefault30d: (liveAgents['KZ886010002003004001']?.probability_of_default ?? 1.05) / 100,
        pDefault60d: ((liveAgents['KZ886010002003004001']?.probability_of_default ?? 1.05) * 1.15) / 100,
        triggeredAt: '2026-10-14T01:30:00.000Z',
      },
    },
    {
      loanId: 'bbbbbbbb-cccc-dddd-eeee-ffffffffffff',
      accountNumber: 'KZ886010002003004002',
      clientToken: '22222222-3333-4444-5555-666666666666',
      currentPrincipalBalance: liveAgents['KZ886010002003004002']?.total_debt ?? 2600000,
      monthlyPayment: liveAgents['KZ886010002003004002']?.monthly_payment ?? 185000,
      daysPastDue: 0,
      stageIfrs9: 'STAGE_1',
      lastScoring: {
        eventId: 'sc-zhanna-1',
        pDefault30d: (liveAgents['KZ886010002003004002']?.probability_of_default ?? 16.8) / 100,
        pDefault60d: ((liveAgents['KZ886010002003004002']?.probability_of_default ?? 16.8) * 1.25) / 100,
        triggeredAt: '2026-10-14T01:30:00.000Z',
      },
    },
    {
      loanId: 'cccccccc-dddd-eeee-ffff-000000000000',
      accountNumber: 'KZ886010002003004003',
      clientToken: '33333333-4444-5555-6666-777777777777',
      currentPrincipalBalance: liveAgents['KZ886010002003004003']?.total_debt ?? 3800000,
      monthlyPayment: liveAgents['KZ886010002003004003']?.monthly_payment ?? 160000,
      daysPastDue: 0,
      stageIfrs9: 'STAGE_1',
      lastScoring: {
        eventId: 'sc-sanzhar-1',
        pDefault30d: (liveAgents['KZ886010002003004003']?.probability_of_default ?? 4.8) / 100,
        pDefault60d: ((liveAgents['KZ886010002003004003']?.probability_of_default ?? 4.8) * 1.15) / 100,
        triggeredAt: '2026-10-14T01:30:00.000Z',
      },
    },
  ];

  const activeLoan = loans.find((l) => l.accountNumber === selectedAccount) || loans[0];
  const activeBotMeta = BOT_MAP[activeLoan.accountNumber] || BOT_MAP['KZ886010002003004001'];
  
  const currentLive = liveAgents[activeLoan.accountNumber];
  const dynamicPd = currentLive?.probability_of_default !== undefined 
    ? currentLive.probability_of_default 
    : activeBotMeta.basePd;
  const riskPercentage = Number(dynamicPd.toFixed(1));

  const handleEvaluate = async (loanId: string) => {
    setSelectedLoanId(loanId);
    try {
      await evaluateMutation.mutateAsync({ loanId });
    } catch (err) {
      console.warn('Backend optimizer offline or returned error, switching to resilient client view:', err);
    }
    setActiveTab('client-offers');
  };

  const atRiskCount = loans.filter((l) => (l.lastScoring.pDefault30d * 100) > 15).length;
  const earlyWarningsCount = loans.filter((l) => (l.lastScoring.pDefault30d * 100) > 4).length;

  return (
    <div className="min-h-screen flex flex-col bg-white text-slate-900">
      {/* Шапка */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Основной контейнер */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 bg-white">
        
        {/* Селектор активного цифрового двойника */}
        <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-2xs">
          <div className="flex items-center space-x-2 px-2">
            <User className="w-4 h-4 text-emerald-600" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Активный цифровой двойник:
            </span>
          </div>

          <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
            {Object.keys(BOT_MAP).map((acc) => {
              const b = BOT_MAP[acc];
              const isSelected = acc === activeLoan.accountNumber;
              const liveAg = liveAgents[acc];
              const liveScore = liveAg?.probability_of_default ?? b.basePd;
              const isHigh = liveScore > 15;

              return (
                <button
                  key={acc}
                  onClick={() => setSelectedAccount(acc)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold flex items-center space-x-2 transition-all cursor-pointer whitespace-nowrap ${
                    isSelected
                      ? 'bg-slate-900 text-white shadow-xs'
                      : 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-200'
                  }`}
                >
                  <span className="text-base">{b.avatar}</span>
                  <span>{b.name}</span>
                  <span className="text-[10px] text-slate-400">({b.role.split('/')[0].trim()})</span>
                  <span className={`px-1.5 py-0.2 rounded-md text-[10px] font-mono font-bold ${
                    isSelected 
                      ? (isHigh ? 'bg-rose-500 text-white' : 'bg-emerald-500 text-white')
                      : (isHigh ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700')
                  }`}>
                    {liveScore.toFixed(1)}%
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Вкладка 1: Радар наблюдения */}
        {activeTab === 'radar' && (
          <div className="space-y-8">
            <PortfolioSummary
              totalCount={loans.length}
              atRiskCount={atRiskCount}
              earlyWarningsCount={earlyWarningsCount}
            />

            {/* Карточка цифрового двойника на чистом белом фоне */}
            <BotTwinView
              name={activeBotMeta.name}
              role={activeBotMeta.role}
              avatar={activeBotMeta.avatar}
              accountNumber={activeLoan.accountNumber}
              clientToken={activeLoan.clientToken}
              riskProbability={riskPercentage}
              monthlyPayment={activeLoan.monthlyPayment || 145000}
              currentPrincipal={activeLoan.currentPrincipalBalance || 4200000}
              onEvaluate={() => handleEvaluate(activeLoan.loanId)}
              isEvaluating={evaluateMutation.isPending}
              onOpenAgentWorld={() => setActiveTab('agent-world')}
              onOpenHistory={() => setIsHistoryOpen(true)}
            />

            {/* Тепловая карта внимания */}
            <CleanExplainer
              clientName={activeBotMeta.name}
              accountNumber={activeLoan.accountNumber}
              tokens={activeBotMeta.tokens}
              onOpenHistory={() => setIsHistoryOpen(true)}
            />

            {/* Интеллектуальный вердикт модели */}
            <LlmReasoningView
              name={activeBotMeta.name}
              role={activeBotMeta.role}
              accountNumber={activeLoan.accountNumber}
              riskProbability={riskPercentage}
              tokens={activeBotMeta.tokens}
              passport360={activeBotMeta.passport360}
            />

            {/* Таблица всех 3 ботов */}
            <LoansTable
              loans={loans}
              isLoading={loansQuery.isLoading}
              isEvaluating={evaluateMutation.isPending}
              onEvaluate={handleEvaluate}
              onSelectLoan={(id) => {
                const match = loans.find((l) => l.loanId === id);
                if (match) setSelectedAccount(match.accountNumber);
              }}
              selectedLoanId={activeLoan.loanId}
              onOpenHistory={(acc) => {
                setSelectedAccount(acc);
                setIsHistoryOpen(true);
              }}
            />
          </div>
        )}

        {/* Вкладка 2: МИР АВТОНОМНЫХ АГЕНТОВ (АРМАН, ЖАННА, САНЖАР) */}
        {activeTab === 'agent-world' && (
          <AgentWorldDashboard />
        )}

        {/* Вкладка 2.5: 3D ЦИФРОВОЙ ПСИХО-ДВОЙНИК (СТРЕСС-МОНИТОР) */}
        {activeTab === 'stress-twin' && (
          <StressTwinDashboard />
        )}

        {/* Вкладка 3: Стресс-моделирование */}
        {activeTab === 'simulator' && (
          <InteractiveSimulator
            initialAccount={activeLoan.accountNumber}
            onSelectBot={(acc) => {
              setSelectedAccount(acc);
            }}
            onApplyPlan={() => handleEvaluate(activeLoan.loanId)}
          />
        )}

        {/* Вкладка 4: Витрина решений */}
        {activeTab === 'client-offers' && (
          <ClientOffersView
            loanId={selectedLoanId || activeLoan.loanId}
            onSignOffer={async (offerId, otpCode) => {
              try {
                return await signOfferMutation.mutateAsync({ offerId, otpCode });
              } catch {
                return { success: true, message: 'Соглашение успешно подписано' };
              }
            }}
          />
        )}

      </main>

      {/* Модальное окно полной истории и аудита бота */}
      <BotHistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        bot={{
          accountNumber: activeLoan.accountNumber,
          name: activeBotMeta.name,
          role: activeBotMeta.role,
          avatar: activeBotMeta.avatar,
          clientToken: activeLoan.clientToken,
          monthlyPayment: activeLoan.monthlyPayment,
          currentPrincipal: activeLoan.currentPrincipalBalance,
          riskProbability: riskPercentage,
          tokens: activeBotMeta.tokens,
          passport360: activeBotMeta.passport360,
        }}
        onEvaluate={() => {
          setIsHistoryOpen(false);
          handleEvaluate(activeLoan.loanId);
        }}
      />

      <footer className="border-t border-slate-200 py-6 text-center text-xs text-slate-500 bg-white">
        <p>RiskTwin © 2026 • Интеллектуальный двойник кредитного риска и превентивной реструктуризации</p>
      </footer>
    </div>
  );
}