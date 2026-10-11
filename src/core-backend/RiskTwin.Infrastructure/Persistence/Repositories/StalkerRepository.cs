using Microsoft.EntityFrameworkCore;
using RiskTwin.Application.Interfaces;
using RiskTwin.Domain.Entities;
using RiskTwin.Infrastructure.Persistence;

namespace RiskTwin.Infrastructure.Persistence.Repositories;

public class StalkerRepository : IStalkerRepository
{
    private readonly RiskTwinDbContext _context;

    public StalkerRepository(RiskTwinDbContext context)
    {
        _context = context;
    }

    public async Task<ClientProfile?> GetProfileByTokenAsync(string clientToken, CancellationToken ct = default)
    {
        return await _context.ClientProfiles
            .Include(p => p.StalkerAlerts)
            .FirstOrDefaultAsync(p => p.ClientToken == clientToken, ct);
    }

    public async Task<List<ClientProfile>> GetWatchedTargetsAsync(int limit = 100, CancellationToken ct = default)
    {
        return await _context.ClientProfiles
            .Include(p => p.StalkerAlerts)
            .OrderByDescending(p => p.CurrentRiskScore)
            .Take(limit)
            .ToListAsync(ct);
    }

    public async Task<List<StalkerTimelineSnapshot>> GetTimelineAsync(string clientToken, int limit = 30, CancellationToken ct = default)
    {
        return await _context.StalkerTimelineSnapshots
            .Where(s => s.ClientToken == clientToken)
            .OrderByDescending(s => s.Timestamp)
            .Take(limit)
            .ToListAsync(ct);
    }

    public async Task<StalkerAlert?> GetAlertByIdAsync(Guid alertId, CancellationToken ct = default)
    {
        return await _context.StalkerAlerts.FirstOrDefaultAsync(a => a.AlertId == alertId, ct);
    }

    public async Task AddAlertAsync(StalkerAlert alert, CancellationToken ct = default)
    {
        await _context.StalkerAlerts.AddAsync(alert, ct);
    }

    public async Task AddTimelineSnapshotAsync(StalkerTimelineSnapshot snapshot, CancellationToken ct = default)
    {
        await _context.StalkerTimelineSnapshots.AddAsync(snapshot, ct);
    }

    public async Task SaveChangesAsync(CancellationToken ct = default)
    {
        await _context.SaveChangesAsync(ct);
    }
}