using RiskTwin.Application.DTOs;

namespace RiskTwin.Application.Interfaces;

public interface IMlInferenceClient
{
    Task<FullAnalysisResultDto> EvaluateAndOptimizeAsync(
        Guid clientToken,
        LoanDetailsDto loanDetails,
        ClientFeaturesDto features,
        CancellationToken cancellationToken = default);
}