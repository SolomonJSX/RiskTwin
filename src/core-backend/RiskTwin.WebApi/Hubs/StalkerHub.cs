using Microsoft.AspNetCore.SignalR;
using RiskTwin.Application.Interfaces;

namespace RiskTwin.WebApi.Hubs;

/// <summary>
/// Двусторонний WebSocket / SignalR хаб системы «Сталкер».
/// Транслирует оповещения риск-офицерам в реальном времени.
/// </summary>
public class StalkerHub : Hub
{
    private readonly ILogger<StalkerHub> _logger;
    private readonly IStalkerEngine _stalkerEngine;

    public StalkerHub(ILogger<StalkerHub> logger, IStalkerEngine stalkerEngine)
    {
        _logger = logger;
        _stalkerEngine = stalkerEngine;
    }

    public override async Task OnConnectedAsync()
    {
        _logger.LogInformation("📡 [STALKER HUB] Подключен терминал риск-офицера: {ConnectionId}", Context.ConnectionId);
        await Groups.AddToGroupAsync(Context.ConnectionId, "RiskOfficersGlobal");
        await base.OnConnectedAsync();
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        _logger.LogInformation("🔌 [STALKER HUB] Терминал риск-офицера отключен: {ConnectionId}", Context.ConnectionId);
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, "RiskOfficersGlobal");
        await base.OnDisconnectedAsync(exception);
    }

    /// <summary>
    /// Встать на персональное слежение за конкретным заемщиком
    /// </summary>
    public async Task TrackClient(string clientToken)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"Watch_{clientToken}");
        _logger.LogInformation("🎯 [STALKER HUB] Офицер {ConnId} встал на слежение за клиентом {Token}", Context.ConnectionId, clientToken);
    }

    /// <summary>
    /// Снять персональное слежение
    /// </summary>
    public async Task UntrackClient(string clientToken)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"Watch_{clientToken}");
    }

    /// <summary>
    /// Подтверждение реакции на алерт прямо из веб-сокета
    /// </summary>
    public async Task AcknowledgeAlert(Guid alertId, string notes)
    {
        string officer = Context.User?.Identity?.Name ?? "RiskOfficer-Live";
        await _stalkerEngine.AcknowledgeAlertAsync(alertId, officer, notes);
        await Clients.Group("RiskOfficersGlobal").SendAsync("AlertAcknowledged", new { AlertId = alertId, Officer = officer });
    }
}