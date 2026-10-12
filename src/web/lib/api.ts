import axios from 'axios';

// Базовый URL к нашему ASP.NET Core бэкенду
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерфейсы данных
export interface LoanSummary {
  loanId: string;
  clientToken: string;
  accountNumber: string;
  currentPrincipalBalance: number;
  monthlyPayment: number;
  daysPastDue: number;
  stageIfrs9: string;
  lastScoring?: {
    eventId: string;
    pDefault30d: number;
    pDefault60d: number;
    triggeredAt: string;
    shapFactorsJson?: string;
    featureSnapshotJson?: string;
  };
}

export interface RestructuringOffer {
  offerId: string;
  scenarioType: string;
  newTenorMonths: number;
  newMonthlyPayment: number;
  gracePeriodMonths: number;
  npvRecoveryRate: number;
  kdnPostRestructure: number;
  status: string;
  expiresAt: string;
}

export interface StalkerTarget {
  clientToken: string;
  segment: string;
  financialLoad: number; // КДН
  riskProbability: number; // PD
  lastAlertReason: string;
  isUnderWatch: boolean;
  activeLoanId: string;
  currentBalance: number;
  monthlyPayment: number;
}

export interface StressSimulateRequest {
  clientToken: string;
  eventType: string; // "SALARY_DROP", "MICROLOAN_TAKEN", "HIGH_EXPENSE"
  deltaValue: number;
  comment: string;
}

// Функции запросов
export const api = {
  // Получить список займов (портфель)
  getLoans: async (): Promise<LoanSummary[]> => {
    const { data } = await apiClient.get('/api/RiskOfficer/loans');
    return data;
  },

  // Запустить ИИ-оценку и подбор плана
  evaluateLoan: async (loanId: string, income: number = 450000) => {
    const { data } = await apiClient.post(`/api/RiskOfficer/evaluate/${loanId}?clientMonthlyIncome=${income}`);
    return data;
  },

  // Получить предложения для клиента
  getOffers: async (loanId: string): Promise<RestructuringOffer[]> => {
    const { data } = await apiClient.get(`/api/DboClient/offers/${loanId}`);
    return data;
  },

  // Подписать оффер по OTP
  signOffer: async (offerId: string, otpCode: string) => {
    const { data } = await apiClient.post('/api/DboClient/sign', { offerId, otpCode });
    return data;
  },

  // Запустить стресс-симуляцию (демо для жюри)
  simulateStress: async (payload: StressSimulateRequest) => {
    const { data } = await apiClient.post('/api/Stalker/simulate-event', payload);
    return data;
  },

  // Получить цели под наблюдением
  getTargets: async () => {
    const { data } = await apiClient.get('/api/Stalker/targets');
    return data;
  },

  // История изменений заемщика
  getTimeline: async (clientToken: string) => {
    const { data } = await apiClient.get(`/api/Stalker/timeline/${clientToken}`);
    return data;
  },
};