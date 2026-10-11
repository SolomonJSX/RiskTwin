using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RiskTwin.Domain.Entities;

/// <summary>
/// Профиль физического лица (заемщика банка) для системы «Сталкер».
/// </summary>
[Table("client_profiles")]
public class ClientProfile
{
    [Key]
    [Column("client_token")]
    [MaxLength(100)]
    public string ClientToken { get; set; } = string.Empty;

    [Required]
    [Column("iin")]
    [MaxLength(12)]
    public string Iin { get; set; } = string.Empty;

    [Required]
    [Column("full_name")]
    [MaxLength(200)]
    public string FullName { get; set; } = string.Empty;

    [Column("age")]
    public int Age { get; set; }

    [Column("gender")]
    [MaxLength(10)]
    public string Gender { get; set; } = "MALE";

    [Column("city")]
    [MaxLength(100)]
    public string City { get; set; } = "Алматы";

    [Column("employment_type")]
    [MaxLength(50)]
    public string EmploymentType { get; set; } = "OFFICIAL_EMPLOYED";

    [Column("industry")]
    [MaxLength(100)]
    public string Industry { get; set; } = "Ритейл";

    [Column("declared_income")]
    public decimal DeclaredIncome { get; set; }

    [Column("archetype")]
    [MaxLength(50)]
    public string Archetype { get; set; } = "STABLE";

    [Column("stress_narrative")]
    public string? StressNarrative { get; set; }

    /// <summary>
    /// Флаг активного наблюдения в системе «Сталкер» (поставлен ли на радар)
    /// </summary>
    [Column("is_under_stalker_watch")]
    public bool IsUnderStalkerWatch { get; set; } = true;

    [Column("current_risk_score")]
    public double CurrentRiskScore { get; set; } = 0.05;

    [Column("risk_level")]
    [MaxLength(20)]
    public string RiskLevel { get; set; } = "GREEN";

    [Column("created_at")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    [Column("updated_at")]
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    // Навигационные свойства
    public virtual ICollection<StalkerAlert> StalkerAlerts { get; set; } = new List<StalkerAlert>();
    public virtual ICollection<StalkerTimelineSnapshot> TimelineSnapshots { get; set; } = new List<StalkerTimelineSnapshot>();
}