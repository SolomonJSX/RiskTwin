import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, StressSimulateRequest } from '@/lib/api';

export const useRiskTwin = () => {
  const queryClient = useQueryClient();

  // Загрузка списка кредитов
  const loansQuery = useQuery({
    queryKey: ['loans'],
    queryFn: api.getLoans,
    refetchInterval: 10000,
  });

  // Загрузка наблюдаемых клиентов (Сталкер)
  const targetsQuery = useQuery({
    queryKey: ['stalker-targets'],
    queryFn: api.getTargets,
    refetchInterval: 10000,
  });

  // Запуск ИИ оценки и оптимизации
  const evaluateMutation = useMutation({
    mutationFn: ({ loanId, income }: { loanId: string; income?: number }) =>
      api.evaluateLoan(loanId, income),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loans'] });
      queryClient.invalidateQueries({ queryKey: ['offers'] });
    },
  });

  // Симуляция стресс-события
  const simulateStressMutation = useMutation({
    mutationFn: (request: StressSimulateRequest) => api.simulateStress(request),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loans'] });
      queryClient.invalidateQueries({ queryKey: ['stalker-targets'] });
    },
  });

  // Подписание оффера клиентом
  const signOfferMutation = useMutation({
    mutationFn: ({ offerId, otpCode }: { offerId: string; otpCode: string }) =>
      api.signOffer(offerId, otpCode),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['offers'] });
      queryClient.invalidateQueries({ queryKey: ['loans'] });
    },
  });

  return {
    loansQuery,
    targetsQuery,
    evaluateMutation,
    simulateStressMutation,
    signOfferMutation,
  };
};

export const useOffers = (loanId: string | null) => {
  return useQuery({
    queryKey: ['offers', loanId],
    queryFn: () => (loanId ? api.getOffers(loanId) : Promise.resolve([])),
    enabled: Boolean(loanId),
  });
};