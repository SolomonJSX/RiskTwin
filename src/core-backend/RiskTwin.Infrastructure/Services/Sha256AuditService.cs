using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using RiskTwin.Application.Interfaces;
using RiskTwin.Domain.Entities;
using RiskTwin.Domain.Enums;
using RiskTwin.Infrastructure.Persistence;

namespace RiskTwin.Infrastructure.Services;

public class Sha256AuditService : IAuditService
{
    private readonly RiskTwinDbContext _context;
    public Sha256AuditService(RiskTwinDbContext context) => _context = context;

    public async Task LogAsync(
        Guid loanId,
        Guid? offerId,
        AuditAction action,
        ActorType actorType,
        string actorId,
        object payload,
        CancellationToken cancellationToken = default)
    {
        var json = JsonSerializer.Serialize(payload);
        var hashBytes = SHA256.HashData(Encoding.UTF8.GetBytes(json));
        var hashHex = Convert.ToHexString(hashBytes).ToLowerInvariant();

        var entry = new ComplianceAuditLog
        {
            LoanId = loanId,
            OfferId = offerId,
            Action = action,
            ActorType = actorType,
            ActorId = actorId,
            PayloadHash = hashHex,
            LoggedAt = DateTime.UtcNow
        };

        await _context.ComplianceAuditLogs.AddAsync(entry, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
    }
}