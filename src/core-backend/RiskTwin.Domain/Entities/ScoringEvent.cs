namespace RiskTwin.Domain.Entities;

public class ScoringEvent
{
    public Guid EventId { get; set; } = Guid.NewGuid();
    public Guid LoanId { get; set; }
    public float PDefault30d { get; set; }
    public float PDefault60d { get; set; }
    public string ModelVersion { get; set; } = "LightGBM_v1";
    public string ShapFactorsJson { get; set; } = "[]"; // XAI факторы
    public string FeatureSnapshotJson { get; set; } = "{}";
    public DateTime TriggeredAt { get; set; } = DateTime.UtcNow;

    public Loan Loan { get; set; } = null!;
    public List<RestructuringOffer> Offers { get; set; } = new();
}