using RiskTwin.Application.DTOs;

namespace RiskTwin.Application.Interfaces;

public interface IStalkerEngine
{
    /// <summary>
    /// Обработка входящего телеметрического события в реальном времени,
    /// вычисление дельты ΔState, запуск Root Cause анализа и генерация алерта.
    /// </summary>
    Task<StalkerAnalysisResult> ProcessTelemetryEventAsync(
        StalkerTelemetryEventDto telemetryEvent,
        CancellationToken ct = default);

    /// <summary>
    /// Получить список всех заемщиков под активным наблюдением «Сталкера».
    /// </summary>
    Task<List<StalkerTargetDto>> GetWatchedTargetsAsync(CancellationToken ct = default);

    /// <summary>
    /// Получить хронологическую ленту изменений (Timeline) по конкретному человеку.
    /// </summary>
    Task<List<StalkerTimelineItemDto>> GetClientTimelineAsync(string clientToken, CancellationToken ct = default);

    /// <summary>
    /// Поставить/снять клиента с активного наблюдения.
    /// </summary>
    Task<bool> ToggleWatchStatusAsync(string clientToken, bool isWatched, CancellationToken ct = default);

    /// <summary>
    /// Подтверждение реакции риск-офицера на алерт (Acknowledge).
    /// </summary>
    Task<bool> AcknowledgeAlertAsync(Guid alertId, string officerName, string? notes, CancellationToken ct = default);
}