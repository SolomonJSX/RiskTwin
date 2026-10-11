using RiskTwin.Domain.Enums;

namespace RiskTwin.Domain.Entities;

public class ComplianceAuditLog
{
    public long LogId { get; set; }
    public Guid? OfferId { get; set; }
    public Guid LoanId { get; set; }
    public AuditAction Action { get; set; }
    public ActorType ActorType { get; set; }
    public string ActorId { get; set; } = string.Empty;
    public string PayloadHash { get; set; } = string.Empty; // SHA-256
    public DateTime LoggedAt { get; set; } = DateTime.UtcNow;
}