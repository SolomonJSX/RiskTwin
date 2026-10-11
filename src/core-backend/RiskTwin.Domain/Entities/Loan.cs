using System.ComponentModel.DataAnnotations.Schema;

namespace RiskTwin.Domain.Entities;

public class Loan
{
    public Guid LoanId { get; set; } = Guid.NewGuid();
    public Guid ClientToken { get; set; }
    public string AccountNumber { get; set; } = string.Empty;
    public decimal OriginalPrincipal { get; set; }
    public decimal CurrentPrincipalBalance { get; set; }
    public decimal InterestRate { get; set; }
    public decimal EffectiveRateGesv { get; set; } // ГЭСВ (%)
    public decimal MonthlyPayment { get; set; }
    public DateOnly MaturityDate { get; set; }
    public int DaysPastDue { get; set; } = 0;
    public string StageIfrs9 { get; set; } = "STAGE_1"; // STAGE_1, STAGE_2, STAGE_3
    public string Status { get; set; } = "ACTIVE";
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public Account Account { get; set; } = null!;
    public List<ScoringEvent> ScoringEvents { get; set; } = new();
}