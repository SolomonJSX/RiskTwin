using RiskTwin.Domain.Enums;

namespace RiskTwin.Domain.Entities;

public class RestructuringOffer
{
    public Guid OfferId { get; set; } = Guid.NewGuid();
    public Guid EventId { get; set; }
    public RestructuringScenarioType ScenarioType { get; set; }
    public int NewTenorMonths { get; set; }
    public decimal NewMonthlyPayment { get; set; }
    public int GracePeriodMonths { get; set; } = 0;
    public decimal NpvRecoveryEst { get; set; }
    public decimal KdnPostRestructure { get; set; }
    public OfferStatus Status { get; set; } = OfferStatus.Offered;
    public DateTime ExpiresAt { get; set; }
    public DateTime? SignedAt { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ScoringEvent ScoringEvent { get; set; } = null!;
}