using RiskTwin.Domain.Enums;

namespace RiskTwin.Application.Interfaces;

public interface IAuditService
{
    Task LogAsync(
        Guid loanId,
        Guid? offerId,
        AuditAction action,
        ActorType actorType,
        string actorId,
        object payload,
        CancellationToken cancellationToken = default);
}