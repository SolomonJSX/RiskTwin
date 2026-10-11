using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using RiskTwin.WebApi.Hubs;

namespace RiskTwin.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class StalkerController : ControllerBase
{
    private readonly IStalkerEngine _stalkerEngine;
    private readonly IHubContext<StalkerHub> _hubContext;
    private readonly ILogger<StalkerController> _logger;

    public StalkerController(
        IStalkerEngine stalkerEngine,
        IHubContext<StalkerHub> hubContext,
        ILogger<StalkerController> logger)
    {
        _stalkerEngine = stalkerEngine;
        _hubContext = hubContext;
        _logger = logger;
    }

    /// <summary>
    /// Список клиентов под активным наблюдением «Сталкера»
    /// </summary>
    [HttpGet("targets")]
    public async Task<IActionResult> GetTargets(CancellationToken ct)
    {
        var targets = await _stalkerEngine.GetWatchedTargetsAsync(ct);
        return Ok(targets);
    }

    /// <summary>
    /// Хронологическая шкала (Timeline) изменений и дельт состояния заемщика
    /// </summary>
    [HttpGet("timeline/{clientToken}")]
    public async Task<IActionResult> GetTimeline(string clientToken, CancellationToken ct)
    {
        var timeline = await _stalkerEngine.GetClientTimelineAsync(clientToken, ct);
        return Ok(timeline);
    }

    /// <summary>
    /// Поставить клиента на радар / снять с радара
    /// </summary>
    [HttpPost("watch")]
    public async Task<IActionResult> ToggleWatch(
        [FromQuery] string clientToken,
        [FromQuery] bool isWatched,
        CancellationToken ct)
    {
        var success = await _stalkerEngine.ToggleWatchStatusAsync(clientToken, isWatched, ct);
        return Ok(new { Success = success, ClientToken = clientToken, IsWatched = isWatched });
    }

    /// <summary>
    /// Подтверждение обработки алерта риск-офицером (Acknowledge)
    /// </summary>
    [HttpPost("acknowledge/{alertId:guid}")]
    public async Task<IActionResult> Acknowledge(
        Guid alertId,
        [FromQuery] string officerName = "RiskOfficer-Admin",
        [FromQuery] string? notes = null,
        CancellationToken ct = default)
    {
        var success = await _stalkerEngine.AcknowledgeAlertAsync(alertId, officerName, notes, ct);
        if (success)
        {
            await _hubContext.Clients.Group("RiskOfficersGlobal").SendAsync("AlertAcknowledged", new
            {
                AlertId = alertId,
                AcknowledgedBy = officerName,
                Notes = notes
            }, ct);
        }
        return Ok(new { Success = success, AlertId = alertId });
    }

    /// <summary>
    /// 🚀 КИЛЛЕР-ФИЧА ДЛЯ ДЕМО ЖЮРИ: Эмулятор стресс-события в реальном времени.
    /// Перехватывает шок, вычисляет дельту, фиксирует причину и мгновенно пушит алерт в SignalR!
    /// </summary>
    [HttpPost("simulate-event")]
    public async Task<IActionResult> SimulateEvent(
        [FromBody] StalkerTelemetryEventDto telemetryEvent,
        CancellationToken ct)
    {
        _logger.LogInformation("⚡ [STALKER] Поступило стресс-событие: {EventType} для {ClientToken}", 
            telemetryEvent.EventType, telemetryEvent.ClientToken);

        var result = await _stalkerEngine.ProcessTelemetryEventAsync(telemetryEvent, ct);

        // Мгновенная трансляция в SignalR для всех подключенных терминалов риск-офицеров
        if (result.AlertTriggered)
        {
            await _hubContext.Clients.Group("RiskOfficersGlobal").SendAsync("StalkerAlertReceived", result, ct);
            await _hubContext.Clients.Group($"Watch_{result.ClientToken}").SendAsync("PersonalAlertReceived", result, ct);
        }

        return Ok(new
        {
            Success = true,
            Analysis = result,
            Message = "Событие обработано движком Сталкер, алерт доставлен в реальном времени"
        });
    }
}