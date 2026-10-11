using RiskTwin.Application.DTOs;

namespace RiskTwin.Application.Interfaces;

public interface IFeatureStore
{
    Task<ClientFeaturesDto> GetFeaturesAsync(Guid clientToken, CancellationToken cancellationToken = default);
}