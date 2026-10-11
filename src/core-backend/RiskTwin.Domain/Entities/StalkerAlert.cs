using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RiskTwin.Domain.Entities;

/// <summary>
/// Мгновенное оповещение системы наблюдения «Сталкер» с точной фиксацией причины.
/// </summary>
[Table("stalker_alerts")]
public class StalkerAlert
{
    [Key]
    [Column("alert_id")]
    public Guid AlertId { get; set; } = Guid.NewGuid();

    [Required]
    [Column("client_token")]
    [MaxLength(100)]
    public string ClientToken { get; set; } = string.Empty;

    [Column("loan_id")]
    public Guid? LoanId { get; set; }

    [Required]
    [Column("trigger_type")]
    [MaxLength(50)]
    public string TriggerType { get; set; } = string.Empty; // MFO_TRANSFER, SALARY_DELAY, DBO_NIGHT_ANXIETY, BNPL_SURGE

    [Column("severity")]
    [MaxLength(20)]
    public string Severity { get; set; } = "WARNING"; // INFO, WARNING, CRITICAL

    [Column("previous_risk_score")]
    public double PreviousRiskScore { get; set; }

    [Column("new_risk_score")]
    public double NewRiskScore { get; set; }

    [Column("delta_risk")]
    public double DeltaRisk { get; set; } // NewRiskScore - PreviousRiskScore

    [Required]
    [Column("reason_ru")]
    public string ReasonRu { get; set; } = string.Empty;

    [Column("reason_kz")]
    public string? ReasonKz { get; set; }

    [Column("recommended_action")]
    public string? RecommendedAction { get; set; }

    [Column("is_acknowledged")]
    public bool IsAcknowledged { get; set; } = false;

    [Column("acknowledged_at")]
    public DateTime? AcknowledgedAt { get; set; }

    [Column("acknowledged_by")]
    [MaxLength(100)]
    public string? AcknowledgedBy { get; set; }

    [Column("created_at")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Навигационные свойства
    [ForeignKey(nameof(ClientToken))]
    public virtual ClientProfile? ClientProfile { get; set; }

    [ForeignKey(nameof(LoanId))]
    public virtual Loan? Loan { get; set; }
}