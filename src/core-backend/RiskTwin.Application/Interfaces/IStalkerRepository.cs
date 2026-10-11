using RiskTwin.Domain.Entities;

namespace RiskTwin.Application.Interfaces;

public interface IStalkerRepository
{
    Task<ClientProfile?> GetProfileByTokenAsync(string clientToken, CancellationToken ct = default);
    Task<List<ClientProfile>> GetWatchedTargetsAsync(int limit = 100, CancellationToken ct = default);
    Task<List<StalkerTimelineSnapshot>> GetTimelineAsync(string clientToken, int limit = 30, CancellationToken ct = default);
    Task<StalkerAlert?> GetAlertByIdAsync(Guid alertId, CancellationToken ct = default);
    Task AddAlertAsync(StalkerAlert alert, CancellationToken ct = default);
    Task AddTimelineSnapshotAsync(StalkerTimelineSnapshot snapshot, CancellationToken ct = default);
    Task SaveChangesAsync(CancellationToken ct = default);
}