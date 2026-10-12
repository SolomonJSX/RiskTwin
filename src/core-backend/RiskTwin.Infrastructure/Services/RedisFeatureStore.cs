using System.Globalization;
using Microsoft.Extensions.Logging;
using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using StackExchange.Redis;

namespace RiskTwin.Infrastructure.Services;

public class RedisFeatureStore : IFeatureStore
{
    private readonly IConnectionMultiplexer? _redis;
    private readonly ILogger<RedisFeatureStore> _logger;

    public RedisFeatureStore(IConnectionMultiplexer? redis, ILogger<RedisFeatureStore> logger)
    {
        _redis = redis;
        _logger = logger;
    }

    public async Task<ClientFeaturesDto> GetFeaturesAsync(Guid clientToken, CancellationToken cancellationToken = default)
    {
        // 1. Попытка прочесть онлайн-вектор из Redis HASH: client:{clientToken}:features
        if (_redis != null && _redis.IsConnected)
        {
            try
            {
                var db = _redis.GetDatabase();
                var key = $"client:{clientToken}:features";
                var hashEntries = await db.HashGetAllAsync(key);

                if (hashEntries != null && hashEntries.Length > 0)
                {
                    var dict = hashEntries.ToDictionary(
                        x => x.Name.ToString(), 
                        x => x.Value.ToString()
                    );

                    double GetD(string name, double def) =>
                        dict.TryGetValue(name, out var s) && double.TryParse(s, NumberStyles.Any, CultureInfo.InvariantCulture, out var v) ? v : def;

                    int GetI(string name, int def) =>
                        dict.TryGetValue(name, out var s) && int.TryParse(s, NumberStyles.Any, CultureInfo.InvariantCulture, out var v) ? v : def;

                    bool GetB(string name, bool def) =>
                        dict.TryGetValue(name, out var s) ? (s == "1" || s.Equals("true", StringComparison.OrdinalIgnoreCase)) : def;

                    _logger.LogInformation("⚡ [FEATURE STORE] Успешно прочитан онлайн-вектор признаков из Redis для клиента {Token}.", clientToken);

                    return new ClientFeaturesDto(
                        SalaryTrendRatio3mVs6m: GetD("salary_trend_ratio_3m_vs_6m", 0.72),
                        SalaryInflowDelayDays: GetI("salary_inflow_delay_days", 5),
                        InflowSourceEntropy: GetD("inflow_source_entropy", 2.0),
                        NetCashflowMargin30d: GetD("net_cashflow_margin_30d", -0.12),
                        AtmCashOutIntensity: GetD("atm_cash_out_intensity", 0.40),
                        CreditToDebitTransferRatio: GetD("credit_to_debit_transfer_ratio", 0.30),
                        EssentialSpendingShareTrend: GetD("essential_spending_share_trend", 0.80),
                        BalanceZeroOutFrequency: GetI("balance_zero_out_frequency", 10),
                        MfoGamblingTagPresence: GetB("mfo_gambling_tag_presence", true),
                        BalanceCheckFrequencySurge: GetD("balance_check_frequency_surge", 3.0),
                        LoanScheduleScreenDwellTime: GetD("loan_schedule_screen_dwell_time", 90.0),
                        SupportChatKeywordVelocity: GetD("support_chat_keyword_velocity", 1.8),
                        MicroloanCalculatorViews: GetI("microloan_calculator_views", 3),
                        DtiDynamicEstimate: GetD("dti_dynamic_estimate", 0.56),
                        ActiveBnplInstallmentCount: GetI("active_bnpl_installment_count", 3),
                        GracePeriodExhaustionRate: GetD("grace_period_exhaustion_rate", 0.88),
                        EarlyPaymentDecayDays: GetI("early_payment_decay_days", 4),
                        MedianDailyBalance7d: GetD("median_daily_balance_7d", 15000),
                        MedianDailyBalance30d: GetD("median_daily_balance_30d", 38000),
                        MedianDailyBalance90d: GetD("median_daily_balance_90d", 115000),
                        P2pOutflowSum7d: GetD("p2p_outflow_sum_7d", 42000),
                        P2pOutflowSum30d: GetD("p2p_outflow_sum_30d", 175000),
                        FailedAutopayAttempts30d: GetI("failed_autopay_attempts_30d", 1)
                    );
                }
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "⚠️ [FEATURE STORE] Ошибка связи с Redis, применяем fallback профиль.");
            }
        }

        // 2. Fallback профиль (если Redis временно недоступен или клиент новый)
        return new ClientFeaturesDto(
            SalaryTrendRatio3mVs6m: 0.68,
            SalaryInflowDelayDays: 6,
            InflowSourceEntropy: 2.1,
            NetCashflowMargin30d: -0.15,
            AtmCashOutIntensity: 0.45,
            CreditToDebitTransferRatio: 0.35,
            EssentialSpendingShareTrend: 0.85,
            BalanceZeroOutFrequency: 12,
            MfoGamblingTagPresence: true,
            BalanceCheckFrequencySurge: 3.2,
            LoanScheduleScreenDwellTime: 95.0,
            SupportChatKeywordVelocity: 2.0,
            MicroloanCalculatorViews: 3,
            DtiDynamicEstimate: 0.58,
            ActiveBnplInstallmentCount: 4,
            GracePeriodExhaustionRate: 0.90,
            EarlyPaymentDecayDays: 4,
            MedianDailyBalance7d: 12500,
            MedianDailyBalance30d: 34000,
            MedianDailyBalance90d: 110000,
            P2pOutflowSum7d: 45000,
            P2pOutflowSum30d: 180000,
            FailedAutopayAttempts30d: 1
        );
    }
}