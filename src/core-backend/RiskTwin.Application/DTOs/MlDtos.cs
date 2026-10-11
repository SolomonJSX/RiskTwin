using RiskTwin.Domain.Enums;

namespace RiskTwin.Application.DTOs;

public record LoanDetailsDto(
    decimal RemainingPrincipal,
    decimal InterestRate,
    int RemainingTermMonths,
    decimal CurrentMonthlyPayment,
    decimal EstimatedCapacity
);

public record ClientFeaturesDto(
    double SalaryTrendRatio3mVs6m,
    int SalaryInflowDelayDays,
    double InflowSourceEntropy,
    double NetCashflowMargin30d,
    double AtmCashOutIntensity,
    double CreditToDebitTransferRatio,
    double EssentialSpendingShareTrend,
    int BalanceZeroOutFrequency,
    bool MfoGamblingTagPresence,
    double BalanceCheckFrequencySurge,
    double LoanScheduleScreenDwellTime,
    double SupportChatKeywordVelocity,
    int MicroloanCalculatorViews,
    double DtiDynamicEstimate,
    int ActiveBnplInstallmentCount,
    double GracePeriodExhaustionRate,
    int EarlyPaymentDecayDays,
    double MedianDailyBalance7d,
    double MedianDailyBalance30d,
    double MedianDailyBalance90d,
    double P2pOutflowSum7d,
    double P2pOutflowSum30d,
    int FailedAutopayAttempts30d
);

public record XaiFactorDto(string FeatureName, double ImpactWeight, string HumanReadableReason);

public record ScenarioDto(
    RestructuringScenarioType ScenarioType,
    string Title,
    string Description,
    int NewTenorMonths,
    decimal NewMonthlyPayment,
    int GracePeriodMonths,
    decimal NpvRecoveryEst,
    bool CompliesWithArrfr,
    double DefaultProbabilityUnderPlan
);

public record FullAnalysisResultDto(
    Guid ClientToken,
    float PDefault30d,
    float PDefault60d,
    bool IsHighRisk,
    string RiskLevel,
    int PredictedDaysToDefault,
    List<XaiFactorDto> TopRiskDrivers,
    List<ScenarioDto> Scenarios,
    double SolverExecutionTimeMs
);