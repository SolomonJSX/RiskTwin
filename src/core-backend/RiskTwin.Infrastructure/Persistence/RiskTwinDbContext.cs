using Microsoft.EntityFrameworkCore;
using RiskTwin.Domain.Entities;
using RiskTwin.Domain.Enums;

namespace RiskTwin.Infrastructure.Persistence;

public class RiskTwinDbContext : DbContext
{
    public RiskTwinDbContext(DbContextOptions<RiskTwinDbContext> options) : base(options) { }

    public DbSet<Account> Accounts => Set<Account>();
    public DbSet<Loan> Loans => Set<Loan>();
    public DbSet<ScoringEvent> ScoringEvents => Set<ScoringEvent>();
    public DbSet<RestructuringOffer> RestructuringOffers => Set<RestructuringOffer>();
    public DbSet<ComplianceAuditLog> ComplianceAuditLogs => Set<ComplianceAuditLog>();
    public DbSet<ClientProfile> ClientProfiles => Set<ClientProfile>();
    public DbSet<StalkerAlert> StalkerAlerts => Set<StalkerAlert>();
    public DbSet<StalkerTimelineSnapshot> StalkerTimelineSnapshots => Set<StalkerTimelineSnapshot>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // 1. accounts
        modelBuilder.Entity<Account>(b =>
        {
            b.ToTable("accounts");
            b.HasKey(a => a.ClientToken);
            b.Property(a => a.ClientToken).HasColumnName("client_token");
            b.Property(a => a.Segment).HasColumnName("segment").HasMaxLength(32).HasDefaultValue("MASS");
            b.Property(a => a.CurrentKdn).HasColumnName("current_kdn").HasPrecision(5, 2);
            b.Property(a => a.IsRestructuringActive).HasColumnName("is_restructuring_active").HasDefaultValue(false);
            b.Property(a => a.CreatedAt).HasColumnName("created_at").HasDefaultValueSql("NOW()");
        });

        modelBuilder.Entity<ClientProfile>(entity =>
        {
            entity.HasIndex(e => e.Iin).IsUnique();
            entity.HasIndex(e => e.IsUnderStalkerWatch);
        });

        modelBuilder.Entity<StalkerAlert>(entity =>
        {
            entity.HasIndex(e => e.ClientToken);
            entity.HasIndex(e => e.CreatedAt);
            entity.HasIndex(e => e.IsAcknowledged);
        });

        modelBuilder.Entity<StalkerTimelineSnapshot>(entity =>
        {
            entity.HasIndex(e => new { e.ClientToken, e.Timestamp });
        });

        // 2. loans
        modelBuilder.Entity<Loan>(b =>
        {
            b.ToTable("loans");
            b.HasKey(l => l.LoanId);
            b.Property(l => l.LoanId).HasColumnName("loan_id").HasDefaultValueSql("gen_random_uuid()");
            b.Property(l => l.ClientToken).HasColumnName("client_token");
            b.Property(l => l.AccountNumber).HasColumnName("account_number").HasMaxLength(34);
            b.Property(l => l.OriginalPrincipal).HasColumnName("original_principal").HasPrecision(14, 2);
            b.Property(l => l.CurrentPrincipalBalance).HasColumnName("current_principal_balance").HasPrecision(14, 2);
            b.Property(l => l.InterestRate).HasColumnName("interest_rate").HasPrecision(5, 2);
            b.Property(l => l.EffectiveRateGesv).HasColumnName("effective_rate_gesv").HasPrecision(5, 2);
            b.Property(l => l.MonthlyPayment).HasColumnName("monthly_payment").HasPrecision(12, 2);
            b.Property(l => l.MaturityDate).HasColumnName("maturity_date");
            b.Property(l => l.DaysPastDue).HasColumnName("days_past_due").HasDefaultValue(0);
            b.Property(l => l.StageIfrs9).HasColumnName("stage_ifrs9").HasMaxLength(10).HasDefaultValue("STAGE_1");
            b.Property(l => l.Status).HasColumnName("status").HasMaxLength(20).HasDefaultValue("ACTIVE");
            b.Property(l => l.UpdatedAt).HasColumnName("updated_at").HasDefaultValueSql("NOW()");

            b.HasOne(l => l.Account)
             .WithMany(a => a.Loans)
             .HasForeignKey(l => l.ClientToken)
             .OnDelete(DeleteBehavior.Restrict);

            b.HasIndex(l => l.ClientToken).HasDatabaseName("idx_loans_client");
        });

        // 3. scoring_events
        modelBuilder.Entity<ScoringEvent>(b =>
        {
            b.ToTable("scoring_events");
            b.HasKey(s => s.EventId);
            b.Property(s => s.EventId).HasColumnName("event_id").HasDefaultValueSql("gen_random_uuid()");
            b.Property(s => s.LoanId).HasColumnName("loan_id");
            b.Property(s => s.PDefault30d).HasColumnName("p_default_30d");
            b.Property(s => s.PDefault60d).HasColumnName("p_default_60d");
            b.Property(s => s.ModelVersion).HasColumnName("model_version").HasMaxLength(32);
            b.Property(s => s.ShapFactorsJson).HasColumnName("shap_factors").HasColumnType("jsonb");
            b.Property(s => s.FeatureSnapshotJson).HasColumnName("feature_snapshot").HasColumnType("jsonb");
            b.Property(s => s.TriggeredAt).HasColumnName("triggered_at").HasDefaultValueSql("NOW()");

            b.HasOne(s => s.Loan)
             .WithMany(l => l.ScoringEvents)
             .HasForeignKey(s => s.LoanId)
             .OnDelete(DeleteBehavior.Cascade);

            b.HasIndex(s => s.LoanId).HasDatabaseName("idx_scoring_loan");
        });

        // 4. restructuring_offers
        modelBuilder.Entity<RestructuringOffer>(b =>
        {
            b.ToTable("restructuring_offers");
            b.HasKey(r => r.OfferId);
            b.Property(r => r.OfferId).HasColumnName("offer_id").HasDefaultValueSql("gen_random_uuid()");
            b.Property(r => r.EventId).HasColumnName("event_id");
            b.Property(r => r.ScenarioType).HasColumnName("scenario_type").HasConversion<string>().HasMaxLength(32);
            b.Property(r => r.NewTenorMonths).HasColumnName("new_tenor_months");
            b.Property(r => r.NewMonthlyPayment).HasColumnName("new_monthly_payment").HasPrecision(12, 2);
            b.Property(r => r.GracePeriodMonths).HasColumnName("grace_period_months").HasDefaultValue(0);
            b.Property(r => r.NpvRecoveryEst).HasColumnName("npv_recovery_est").HasPrecision(14, 2);
            b.Property(r => r.KdnPostRestructure).HasColumnName("kdn_post_restructure").HasPrecision(5, 2);
            b.Property(r => r.Status).HasColumnName("status").HasConversion<string>().HasMaxLength(20).HasDefaultValue(OfferStatus.Offered);
            b.Property(r => r.ExpiresAt).HasColumnName("expires_at");
            b.Property(r => r.SignedAt).HasColumnName("signed_at");
            b.Property(r => r.CreatedAt).HasColumnName("created_at").HasDefaultValueSql("NOW()");

            b.HasOne(r => r.ScoringEvent)
             .WithMany(s => s.Offers)
             .HasForeignKey(r => r.EventId)
             .OnDelete(DeleteBehavior.Cascade);

            b.HasIndex(r => r.EventId).HasDatabaseName("idx_offers_event");
            b.HasIndex(r => r.Status).HasDatabaseName("idx_offers_status");
        });

        // 5. compliance_audit_log
        modelBuilder.Entity<ComplianceAuditLog>(b =>
        {
            b.ToTable("compliance_audit_log");
            b.HasKey(c => c.LogId);
            b.Property(c => c.LogId).HasColumnName("log_id").ValueGeneratedOnAdd();
            b.Property(c => c.OfferId).HasColumnName("offer_id");
            b.Property(c => c.LoanId).HasColumnName("loan_id");
            b.Property(c => c.Action).HasColumnName("action").HasConversion<string>().HasMaxLength(64);
            b.Property(c => c.ActorType).HasColumnName("actor_type").HasConversion<string>().HasMaxLength(32);
            b.Property(c => c.ActorId).HasColumnName("actor_id").HasMaxLength(64);
            b.Property(c => c.PayloadHash).HasColumnName("payload_hash").HasMaxLength(64);
            b.Property(c => c.LoggedAt).HasColumnName("logged_at").HasDefaultValueSql("NOW()");
        });
    }

    public async Task SeedClientProfilesFromCsvAsync(string csvPath)
    {
        // 1. Создаем новые таблицы Сталкера, если их еще нет в базе
        await Database.ExecuteSqlRawAsync(@"
            CREATE TABLE IF NOT EXISTS client_profiles (
                client_token VARCHAR(100) PRIMARY KEY,
                iin VARCHAR(12) NOT NULL,
                full_name VARCHAR(200) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10) NOT NULL,
                city VARCHAR(100) NOT NULL,
                employment_type VARCHAR(50) NOT NULL,
                industry VARCHAR(100) NOT NULL,
                declared_income NUMERIC NOT NULL,
                archetype VARCHAR(50) NOT NULL,
                stress_narrative TEXT,
                is_under_stalker_watch BOOLEAN NOT NULL DEFAULT TRUE,
                current_risk_score DOUBLE PRECISION NOT NULL DEFAULT 0.05,
                risk_level VARCHAR(20) NOT NULL DEFAULT 'GREEN',
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS stalker_alerts (
                alert_id UUID PRIMARY KEY,
                client_token VARCHAR(100) NOT NULL REFERENCES client_profiles(client_token) ON DELETE CASCADE,
                loan_id UUID,
                trigger_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) NOT NULL DEFAULT 'WARNING',
                previous_risk_score DOUBLE PRECISION NOT NULL,
                new_risk_score DOUBLE PRECISION NOT NULL,
                delta_risk DOUBLE PRECISION NOT NULL,
                reason_ru TEXT NOT NULL,
                reason_kz TEXT,
                recommended_action TEXT,
                is_acknowledged BOOLEAN NOT NULL DEFAULT FALSE,
                acknowledged_at TIMESTAMP WITH TIME ZONE,
                acknowledged_by VARCHAR(100),
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS stalker_timeline_snapshots (
                snapshot_id UUID PRIMARY KEY,
                client_token VARCHAR(100) NOT NULL REFERENCES client_profiles(client_token) ON DELETE CASCADE,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                risk_score DOUBLE PRECISION NOT NULL,
                delta_pd DOUBLE PRECISION NOT NULL,
                salary_trend DOUBLE PRECISION NOT NULL,
                salary_delay_days INT NOT NULL,
                has_mfo_activity BOOLEAN NOT NULL,
                active_bnpl_count INT NOT NULL,
                dti_estimate DOUBLE PRECISION NOT NULL,
                daily_balance_7d NUMERIC NOT NULL,
                dbo_checks_count INT NOT NULL,
                primary_trigger VARCHAR(100)
            );
        ");

        if (await ClientProfiles.AnyAsync())
        {
            return; // База уже заполнена
        }

        if (!File.Exists(csvPath))
        {
            return;
        }

        var lines = await File.ReadAllLinesAsync(csvPath);
        if (lines.Length <= 1) return;

        var profiles = new List<ClientProfile>();

        for (int i = 1; i < lines.Length; i++)
        {
            var line = lines[i];
            if (string.IsNullOrWhiteSpace(line)) continue;

            var parts = line.Split(',');
            if (parts.Length < 35) continue;

            string clientToken = parts[0].Trim();
            string fullName = parts[1].Trim().Trim('"');
            string iin = parts[2].Trim();
            int.TryParse(parts[3].Trim(), out int age);
            string gender = parts[4].Trim();
            string city = parts[5].Trim();
            string empType = parts[6].Trim();
            string industry = parts[7].Trim();
            decimal.TryParse(parts[8].Trim(), System.Globalization.NumberStyles.Any, System.Globalization.CultureInfo.InvariantCulture, out decimal income);
            string archetype = parts[9].Trim();
            string stressNarrative = parts[10].Trim().Trim('"');
            double.TryParse(parts[parts.Length - 2].Trim(), System.Globalization.NumberStyles.Any, System.Globalization.CultureInfo.InvariantCulture, out double targetDefault);

            double riskScore = targetDefault > 0 ? (0.65 + (i % 30) * 0.01) : (0.05 + (i % 15) * 0.01);
            riskScore = Math.Min(0.99, Math.Round(riskScore, 4));

            var profile = new ClientProfile
            {
                ClientToken = clientToken,
                FullName = string.IsNullOrWhiteSpace(fullName) ? $"Заемщик #{i}" : fullName,
                Iin = string.IsNullOrWhiteSpace(iin) ? $"850101300{i:D3}" : iin,
                Age = age >= 18 ? age : 28,
                Gender = gender,
                City = city,
                EmploymentType = empType,
                Industry = industry,
                DeclaredIncome = income > 0 ? income : 350000m,
                Archetype = archetype,
                StressNarrative = stressNarrative,
                IsUnderStalkerWatch = true,
                CurrentRiskScore = riskScore,
                RiskLevel = riskScore >= 0.60 ? "RED" : (riskScore >= 0.35 ? "YELLOW" : "GREEN"),
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            profiles.Add(profile);
        }

        await ClientProfiles.AddRangeAsync(profiles);
        await SaveChangesAsync();
    }
}