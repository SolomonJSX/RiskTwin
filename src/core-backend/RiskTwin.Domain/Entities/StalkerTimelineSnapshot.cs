using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RiskTwin.Domain.Entities;

/// <summary>
/// Временной срез состояния заемщика (Timeline State) для вычисления дельт ΔState.
/// </summary>
[Table("stalker_timeline_snapshots")]
public class StalkerTimelineSnapshot
{
    [Key]
    [Column("snapshot_id")]
    public Guid SnapshotId { get; set; } = Guid.NewGuid();

    [Required]
    [Column("client_token")]
    [MaxLength(100)]
    public string ClientToken { get; set; } = string.Empty;

    [Column("timestamp")]
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;

    [Column("risk_score")]
    public double RiskScore { get; set; }

    [Column("delta_pd")]
    public double DeltaPd { get; set; }

    [Column("salary_trend")]
    public double SalaryTrend { get; set; }

    [Column("salary_delay_days")]
    public int SalaryDelayDays { get; set; }

    [Column("has_mfo_activity")]
    public bool HasMfoActivity { get; set; }

    [Column("active_bnpl_count")]
    public int ActiveBnplCount { get; set; }

    [Column("dti_estimate")]
    public double DtiEstimate { get; set; }

    [Column("daily_balance_7d")]
    public decimal DailyBalance7d { get; set; }

    [Column("dbo_checks_count")]
    public int DboChecksCount { get; set; }

    [Column("primary_trigger")]
    [MaxLength(100)]
    public string? PrimaryTrigger { get; set; }

    [ForeignKey(nameof(ClientToken))]
    public virtual ClientProfile? ClientProfile { get; set; }
}