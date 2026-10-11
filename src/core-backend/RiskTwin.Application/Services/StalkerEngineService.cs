using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using RiskTwin.Domain.Entities;

namespace RiskTwin.Application.Services;

public class StalkerEngineService : IStalkerEngine
{
    private readonly IStalkerRepository _stalkerRepo;
    private readonly IMlInferenceClient _mlClient;
    private readonly IFeatureStore _featureStore;

    public StalkerEngineService(
        IStalkerRepository stalkerRepo,
        IMlInferenceClient mlClient,
        IFeatureStore featureStore)
    {
        _stalkerRepo = stalkerRepo;
        _mlClient = mlClient;
        _featureStore = featureStore;
    }

    public async Task<StalkerAnalysisResult> ProcessTelemetryEventAsync(
        StalkerTelemetryEventDto telemetryEvent,
        CancellationToken ct = default)
    {
        var profile = await _stalkerRepo.GetProfileByTokenAsync(telemetryEvent.ClientToken, ct);

        if (profile == null)
        {
            throw new KeyNotFoundException($"Заемщик с токеном {telemetryEvent.ClientToken} не найден в реестре Сталкера.");
        }

        double previousRisk = profile.CurrentRiskScore;
        double newRisk = previousRisk;
        string triggerType = telemetryEvent.EventType.ToString();
        string severity = "INFO";
        string reasonRu = string.Empty;
        string reasonKz = string.Empty;
        string recommendedAction = "Мониторинг в штатном режиме";

        switch (telemetryEvent.EventType)
        {
            case StalkerEventType.MfoTransfer:
                newRisk = Math.Min(0.99, previousRisk + 0.42);
                severity = "CRITICAL";
                triggerType = "MFO_TRANSFER";
                reasonRu = $"Зафиксирован перевод {telemetryEvent.Amount:N0} KZT в пользу МФО '{telemetryEvent.MerchantOrRecipient ?? "Микрозайм"}'. Риск долговой спирали.";
                reasonKz = $"'{telemetryEvent.MerchantOrRecipient ?? "Микрозайм"}' МҚҰ пайдасына {telemetryEvent.Amount:N0} KZT аударымы тіркелді. Қарыз қаупі.";
                recommendedAction = "Немедленная превентивная реструктуризация (Кредитные каникулы на 2 мес.)";
                break;

            case StalkerEventType.SalaryDelay:
                int delay = telemetryEvent.DelayDays ?? 7;
                newRisk = Math.Min(0.99, previousRisk + (delay >= 10 ? 0.35 : 0.20));
                severity = delay >= 10 ? "CRITICAL" : "WARNING";
                triggerType = "SALARY_DELAY";
                reasonRu = $"Задержка регулярной зарплаты на {delay} дней от исторической даты выплаты.";
                reasonKz = $"Тұрақты жалақының тарихи төлем күнінен {delay} күнге кешігуі байқалды.";
                recommendedAction = "Предложить перенос даты ежемесячного платежа под новый зарплатный цикл";
                break;

            case StalkerEventType.SalaryCut:
                double drop = telemetryEvent.SalaryDropPercent ?? 30.0;
                newRisk = Math.Min(0.99, previousRisk + (drop >= 30.0 ? 0.38 : 0.18));
                severity = drop >= 30.0 ? "CRITICAL" : "WARNING";
                triggerType = "INCOME_SHOCK";
                reasonRu = $"Падение ежемесячного зарплатного поступления на {drop:F0}%. Рост долговой нагрузки DTI.";
                reasonKz = $"Айлық жалақы түсімінің {drop:F0}%-ға төмендеуі. Қарыз жүктемесінің артуы.";
                recommendedAction = "Пролонгация кредита со снижением ежемесячного платежа на 35%";
                break;

            case StalkerEventType.BnplSurge:
                int bnplCount = telemetryEvent.NewBnplCount ?? 5;
                newRisk = Math.Min(0.99, previousRisk + 0.28);
                severity = "WARNING";
                triggerType = "BNPL_OVERLEVERAGED";
                reasonRu = $"Оформление {bnplCount}-й параллельной рассрочки (Kaspi/Halyk 0-0-24). Исчерпание свободного денежного потока.";
                reasonKz = $"{bnplCount}-ші қатардағы бөліп төлеудің ресімделуі (0-0-24). Қолма-қол ақша ағынының сарқылуы.";
                recommendedAction = "Консолидация рассрочек и кредита в единый комфортный платеж";
                break;

            case StalkerEventType.DboNightAnxiety:
                newRisk = Math.Min(0.99, previousRisk + 0.15);
                severity = "INFO";
                triggerType = "DBO_NIGHT_ANXIETY";
                reasonRu = "Аномальная психоэмоциональная активность: 4+ ночных входа в ДБО и изучение графика погашения.";
                reasonKz = "Түнгі уақытта қосымшаға бірнеше рет кіріп, төлем кестесін қарау бойынша белсенділік байқалды.";
                recommendedAction = "Превентивный пуш в ДБО: «Нужна помощь с платежом? Ознакомьтесь с мерами поддержки»";
                break;

            case StalkerEventType.BalanceZeroOut:
                newRisk = Math.Min(0.99, previousRisk + 0.25);
                severity = "WARNING";
                triggerType = "LIQUIDITY_GAP";
                reasonRu = $"Критическое обнуление остатка на счете (< 1 000 KZT) за 10 дней до планового платежа.";
                reasonKz = $"Жоспарлы төлемге дейін 10 күн қалғанда шоттағы қалдықтың нөлге жетуі (< 1 000 KZT).";
                recommendedAction = "Временный грейс-период на 1 месяц";
                break;

            default:
                newRisk = previousRisk;
                reasonRu = "Событие зарегистрировано без существенного изменения скора";
                reasonKz = "Оқиға елеулі өзгеріссіз тіркелді";
                break;
        }

        double deltaRisk = Math.Round(newRisk - previousRisk, 4);
        newRisk = Math.Round(newRisk, 4);

        profile.CurrentRiskScore = newRisk;
        profile.RiskLevel = newRisk >= 0.60 ? "RED" : (newRisk >= 0.35 ? "YELLOW" : "GREEN");
        profile.UpdatedAt = DateTime.UtcNow;

        Guid? alertId = null;
        bool isAlertTriggered = deltaRisk >= 0.10 || newRisk >= 0.50;

        if (isAlertTriggered)
        {
            var alert = new StalkerAlert
            {
                AlertId = Guid.NewGuid(),
                ClientToken = profile.ClientToken,
                LoanId = null,
                TriggerType = triggerType,
                Severity = severity,
                PreviousRiskScore = previousRisk,
                NewRiskScore = newRisk,
                DeltaRisk = deltaRisk,
                ReasonRu = reasonRu,
                ReasonKz = reasonKz,
                RecommendedAction = recommendedAction,
                IsAcknowledged = false,
                CreatedAt = DateTime.UtcNow
            };

            await _stalkerRepo.AddAlertAsync(alert, ct);
            alertId = alert.AlertId;
        }

        var snapshot = new StalkerTimelineSnapshot
        {
            SnapshotId = Guid.NewGuid(),
            ClientToken = profile.ClientToken,
            Timestamp = DateTime.UtcNow,
            RiskScore = newRisk,
            DeltaPd = deltaRisk,
            DailyBalance7d = telemetryEvent.Amount > 0 && telemetryEvent.EventType == StalkerEventType.BalanceZeroOut 
                ? telemetryEvent.Amount 
                : 35000m,
            DtiEstimate = profile.CurrentRiskScore * 0.8,
            PrimaryTrigger = reasonRu,
            HasMfoActivity = telemetryEvent.EventType == StalkerEventType.MfoTransfer,
            ActiveBnplCount = telemetryEvent.NewBnplCount ?? 1
        };
        await _stalkerRepo.AddTimelineSnapshotAsync(snapshot, ct);

        await _stalkerRepo.SaveChangesAsync(ct);

        return new StalkerAnalysisResult(
            ClientToken: profile.ClientToken,
            AlertTriggered: isAlertTriggered,
            TriggerType: triggerType,
            Severity: severity,
            PreviousRisk: previousRisk,
            NewRisk: newRisk,
            DeltaRisk: deltaRisk,
            ReasonRu: reasonRu,
            ReasonKz: reasonKz,
            RecommendedAction: recommendedAction,
            AlertId: alertId
        );
    }

    public async Task<List<StalkerTargetDto>> GetWatchedTargetsAsync(CancellationToken ct = default)
    {
        var targets = await _stalkerRepo.GetWatchedTargetsAsync(100, ct);

        return targets.Select(p => new StalkerTargetDto(
            ClientToken: p.ClientToken,
            FullName: p.FullName,
            Iin: p.Iin,
            City: p.City,
            Age: p.Age,
            Archetype: p.Archetype,
            DeclaredIncome: p.DeclaredIncome,
            CurrentRiskScore: p.CurrentRiskScore,
            RiskLevel: p.RiskLevel,
            IsUnderWatch: p.IsUnderStalkerWatch,
            TotalAlertsCount: p.StalkerAlerts.Count,
            LastEventAt: p.StalkerAlerts.OrderByDescending(a => a.CreatedAt).FirstOrDefault()?.CreatedAt ?? p.UpdatedAt,
            LastReasonRu: p.StalkerAlerts.OrderByDescending(a => a.CreatedAt).FirstOrDefault()?.ReasonRu ?? p.StressNarrative
        )).ToList();
    }

    public async Task<List<StalkerTimelineItemDto>> GetClientTimelineAsync(string clientToken, CancellationToken ct = default)
    {
        var snapshots = await _stalkerRepo.GetTimelineAsync(clientToken, 30, ct);

        return snapshots.Select(s => new StalkerTimelineItemDto(
            SnapshotId: s.SnapshotId,
            Timestamp: s.Timestamp,
            RiskScore: s.RiskScore,
            DeltaPd: s.DeltaPd,
            EventDescriptionRu: s.PrimaryTrigger ?? "Штатный мониторинг финансового профиля",
            EventDescriptionKz: "Қаржылық бейінді штаттық бақылау",
            Severity: s.RiskScore >= 0.60 ? "CRITICAL" : (s.RiskScore >= 0.35 ? "WARNING" : "INFO"),
            DailyBalance: s.DailyBalance7d,
            Dti: s.DtiEstimate
        )).ToList();
    }

    public async Task<bool> ToggleWatchStatusAsync(string clientToken, bool isWatched, CancellationToken ct = default)
    {
        var profile = await _stalkerRepo.GetProfileByTokenAsync(clientToken, ct);
        if (profile == null) return false;

        profile.IsUnderStalkerWatch = isWatched;
        profile.UpdatedAt = DateTime.UtcNow;
        await _stalkerRepo.SaveChangesAsync(ct);
        return true;
    }

    public async Task<bool> AcknowledgeAlertAsync(Guid alertId, string officerName, string? notes, CancellationToken ct = default)
    {
        var alert = await _stalkerRepo.GetAlertByIdAsync(alertId, ct);
        if (alert == null) return false;

        alert.IsAcknowledged = true;
        alert.AcknowledgedAt = DateTime.UtcNow;
        alert.AcknowledgedBy = officerName;
        await _stalkerRepo.SaveChangesAsync(ct);
        return true;
    }
}