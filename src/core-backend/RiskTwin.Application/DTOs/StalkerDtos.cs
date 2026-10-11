namespace RiskTwin.Application.DTOs;

/// <summary>
/// Типы входящих телеметрических событий заемщика в реальном времени.
/// </summary>
public enum StalkerEventType
{
    MfoTransfer,             // Перевод/оплата в МФО (Займер, Кредит24 и др.)
    SalaryDelay,             // Задержка поступления регулярной зарплаты
    SalaryCut,               // Снижение размера зарплаты
    BnplSurge,               // Оформление новой рассрочки (Kaspi/Halyk 0-0-12/24)
    DboNightAnxiety,         // Ночной вход в ДБО + проверка графика кредита
    BalanceZeroOut,          // Резкое падение остатка на счете ниже критического порога
    SupportChatInquiry       // Вопрос боту/поддержке по реструктуризации/отсрочке
}

/// <summary>
/// Входящее событие для эмуляции или реального стриминга через Kafka/Redpanda.
/// </summary>
public record StalkerTelemetryEventDto(
    string ClientToken,
    StalkerEventType EventType,
    decimal Amount = 0,
    string? MerchantOrRecipient = null,
    int? DelayDays = null,
    int? NewBnplCount = null,
    double? SalaryDropPercent = null,
    string? Metadata = null
);

/// <summary>
/// Результат работы движка Root Cause Analysis.
/// </summary>
public record StalkerAnalysisResult(
    string ClientToken,
    bool AlertTriggered,
    string TriggerType,
    string Severity, // INFO, WARNING, CRITICAL
    double PreviousRisk,
    double NewRisk,
    double DeltaRisk,
    string ReasonRu,
    string ReasonKz,
    string RecommendedAction,
    Guid? AlertId
);

/// <summary>
/// DTO для отображения клиента на радаре «Сталкера» в веб-кабинете риск-офицера.
/// </summary>
public record StalkerTargetDto(
    string ClientToken,
    string FullName,
    string Iin,
    string City,
    int Age,
    string Archetype,
    decimal DeclaredIncome,
    double CurrentRiskScore,
    string RiskLevel,
    bool IsUnderWatch,
    int TotalAlertsCount,
    DateTime LastEventAt,
    string? LastReasonRu
);

/// <summary>
/// Элемент временной шкалы (Timeline) заемщика.
/// </summary>
public record StalkerTimelineItemDto(
    Guid SnapshotId,
    DateTime Timestamp,
    double RiskScore,
    double DeltaPd,
    string EventDescriptionRu,
    string EventDescriptionKz,
    string Severity,
    decimal DailyBalance,
    double Dti
);