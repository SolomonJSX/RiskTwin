using Grpc.Net.Client;
using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using RiskTwin.CoreBackend.Grpc;
using RiskTwin.Domain.Enums;

namespace RiskTwin.Infrastructure.GrpcClients;

public class MlInferenceGrpcClient : IMlInferenceClient
{
    private readonly RestructuringOptimizerService.RestructuringOptimizerServiceClient _client;

    public MlInferenceGrpcClient(string grpcServerUrl = "http://localhost:50051")
    {
        var channel = GrpcChannel.ForAddress(grpcServerUrl);
        _client = new RestructuringOptimizerService.RestructuringOptimizerServiceClient(channel);
    }

    public async Task<FullAnalysisResultDto> EvaluateAndOptimizeAsync(
        Guid clientToken,
        LoanDetailsDto loanDetails,
        ClientFeaturesDto features,
        CancellationToken cancellationToken = default)
    {
        // 1. Формируем запрос
        var request = new FullRestructuringAnalysisRequest
        {
            RiskFeatures = new RiskEvaluationRequest
            {
                ClientToken = clientToken.ToString(),
                SalaryTrendRatio3MVs6M = features.SalaryTrendRatio3mVs6m,
                SalaryInflowDelayDays = features.SalaryInflowDelayDays,
                InflowSourceEntropy = features.InflowSourceEntropy,
                NetCashflowMargin30D = features.NetCashflowMargin30d,
                AtmCashOutIntensity = features.AtmCashOutIntensity,
                CreditToDebitTransferRatio = features.CreditToDebitTransferRatio,
                EssentialSpendingShareTrend = features.EssentialSpendingShareTrend,
                BalanceZeroOutFrequency = features.BalanceZeroOutFrequency,
                MfoGamblingTagPresence = features.MfoGamblingTagPresence,
                BalanceCheckFrequencySurge = features.BalanceCheckFrequencySurge,
                LoanScheduleScreenDwellTime = features.LoanScheduleScreenDwellTime,
                SupportChatKeywordVelocity = features.SupportChatKeywordVelocity,
                MicroloanCalculatorViews = features.MicroloanCalculatorViews,
                DtiDynamicEstimate = features.DtiDynamicEstimate,
                ActiveBnplInstallmentCount = features.ActiveBnplInstallmentCount,
                GracePeriodExhaustionRate = features.GracePeriodExhaustionRate,
                EarlyPaymentDecayDays = features.EarlyPaymentDecayDays,
                MedianDailyBalance7D = features.MedianDailyBalance7d,
                MedianDailyBalance30D = features.MedianDailyBalance30d,
                MedianDailyBalance90D = features.MedianDailyBalance90d,
                P2POutflowSum7D = features.P2pOutflowSum7d,
                P2POutflowSum30D = features.P2pOutflowSum30d,
                FailedAutopayAttempts30D = features.FailedAutopayAttempts30d
            },
            LoanDetails = new OptimizationRequest
            {
                ClientToken = clientToken.ToString(),
                RemainingPrincipal = (double)loanDetails.RemainingPrincipal,
                InterestRate = (double)loanDetails.InterestRate,
                RemainingTermMonths = loanDetails.RemainingTermMonths,
                CurrentMonthlyPayment = (double)loanDetails.CurrentMonthlyPayment,
                EstimatedClientCapacity = (double)loanDetails.EstimatedCapacity
            }
        };

        // 2. Сетевой вызов по gRPC
        var deadline = DateTime.UtcNow.AddSeconds(3); // SLA: максимум 3 секунды на солвер MILP
var response = await _client.EvaluateAndOptimizeAsync(request, deadline: deadline, cancellationToken: cancellationToken);

        // 3. Маппинг ответа в DTO
        var xaiDrivers = response.TopRiskDrivers
            .Select(d => new XaiFactorDto(d.FeatureName, d.ImpactWeight, d.HumanReadableReason))
            .ToList();

        var scenarios = response.Scenarios.Select(s => new ScenarioDto(
            ScenarioType: (RestructuringScenarioType)(int)s.ScenarioType,
            Title: s.Title,
            Description: s.Description,
            NewTenorMonths: s.NewTermMonths,
            NewMonthlyPayment: (decimal)s.NewMonthlyPayment,
            GracePeriodMonths: s.GracePeriodMonths,
            NpvRecoveryEst: (decimal)s.NpvRecoveryRate,
            CompliesWithArrfr: s.CompliesWithArrfr,
            DefaultProbabilityUnderPlan: s.DefaultProbabilityUnderPlan
        )).ToList();

        return new FullAnalysisResultDto(
            ClientToken: clientToken,
            PDefault30d: (float)response.PDefault30D,
            PDefault60d: (float)response.PDefault60D,
            IsHighRisk: response.IsHighRisk,
            RiskLevel: response.RiskLevel.ToString(),
            PredictedDaysToDefault: response.PredictedDaysToDefault,
            TopRiskDrivers: xaiDrivers,
            Scenarios: scenarios,
            SolverExecutionTimeMs: response.SolverExecutionTimeMs
        );
    }
}