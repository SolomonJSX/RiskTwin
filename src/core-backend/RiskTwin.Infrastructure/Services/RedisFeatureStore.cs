using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;

namespace RiskTwin.Infrastructure.Services;

public class RedisFeatureStore : IFeatureStore
{
    // В боевой версии читает ZSET feat:{token}:inflows_daily и счетчики из Redis.
    // Если клиент новый или ключа нет, возвращает реалистичный профиль риска из телеметрии.
    public Task<ClientFeaturesDto> GetFeaturesAsync(Guid clientToken, CancellationToken cancellationToken = default)
    {
        var sampleFeatures = new ClientFeaturesDto(
            SalaryTrendRatio3mVs6m: 0.68,              // Падение зарплаты (сильный триггер < 0.8)
            SalaryInflowDelayDays: 6,                 // Задержка выплаты 6 дней
            InflowSourceEntropy: 2.1,
            NetCashflowMargin30d: -0.15,               // Отрицательный кэшфлоу (проедает подушку)
            AtmCashOutIntensity: 0.45,
            CreditToDebitTransferRatio: 0.35,          // Переводы с кредитки на дебет
            EssentialSpendingShareTrend: 0.85,
            BalanceZeroOutFrequency: 12,              // 12 дней остаток был меньше 1000 KZT
            MfoGamblingTagPresence: true,             // Срабатывание шлюза МФО
            BalanceCheckFrequencySurge: 3.2,          // Всплеск тревожности в ДБО
            LoanScheduleScreenDwellTime: 95.0,        // 95 сек на экране графика
            SupportChatKeywordVelocity: 2.0,
            MicroloanCalculatorViews: 3,
            DtiDynamicEstimate: 0.58,                 // DTI 58% (> 50% норматив АРРФР)
            ActiveBnplInstallmentCount: 4,            // 4 параллельные рассрочки 0-0-12
            GracePeriodExhaustionRate: 0.90,
            EarlyPaymentDecayDays: 4,
            MedianDailyBalance7d: 12500,
            MedianDailyBalance30d: 34000,
            MedianDailyBalance90d: 110000,
            P2pOutflowSum7d: 45000,
            P2pOutflowSum30d: 180000,
            FailedAutopayAttempts30d: 1
        );

        return Task.FromResult(sampleFeatures);
    }
}