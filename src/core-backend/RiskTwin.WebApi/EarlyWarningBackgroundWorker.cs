using Microsoft.EntityFrameworkCore;
using RiskTwin.Application.Services;
using RiskTwin.Infrastructure.Persistence;

namespace RiskTwin.WebApi;

public class EarlyWarningBackgroundWorker : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<EarlyWarningBackgroundWorker> _logger;
    private const double EarlyInterventionThreshold = 0.40; // Порог раннего вмешательства (40%)

    public EarlyWarningBackgroundWorker(
        IServiceProvider serviceProvider,
        ILogger<EarlyWarningBackgroundWorker> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("🚀 [WORKER] Фоновый конвейер раннего предупреждения запущен в банковском контуре.");

        // Небольшая пауза в 3 секунды перед первым прогоном (чтобы EF Core успел применить сиды)
        await Task.Delay(TimeSpan.FromSeconds(3), stoppingToken);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                using var scope = _serviceProvider.CreateScope();
                var dbContext = scope.ServiceProvider.GetRequiredService<RiskTwinDbContext>();
                var workflowService = scope.ServiceProvider.GetRequiredService<RestructuringWorkflowService>();

                // 1. Извлекаем активные ссуды, у которых еще нет активного процесса реструктуризации
                var candidateLoans = await dbContext.Loans
                    .Include(l => l.Account)
                    .Where(l => l.Status == "ACTIVE" && !l.Account.IsRestructuringActive)
                    .Take(50)
                    .ToListAsync(stoppingToken);

                if (candidateLoans.Any())
                {
                    _logger.LogInformation("🔍 [WORKER] Сканирование портфеля: найдено {Count} активных договоров для скоринга.", candidateLoans.Count);

                    foreach (var loan in candidateLoans)
                    {
                        // 2. Запускаем сквозную сагу: Redis фичи -> gRPC ML -> OR-Tools -> АРРФР
                        // Для демо берем расчетный доход из кредита (например, платеж / 0.35)
                        decimal estimatedIncome = loan.MonthlyPayment > 0 ? (loan.MonthlyPayment / 0.35m) : 450000m;

                        var eventId = await workflowService.ProcessEarlyWarningAsync(loan.LoanId, estimatedIncome, stoppingToken);

                        if (eventId.HasValue)
                        {
                            // 3. Отмечаем аккаунт, чтобы не спамить повторно в следующем цикле
                            loan.Account.IsRestructuringActive = true;
                            await dbContext.SaveChangesAsync(stoppingToken);

                            _logger.LogWarning("⚠️ [WORKER] Кредит {LoanId} (счет {Account}) успешно квалифицирован, сгенерирована триада офферов!", 
                                loan.LoanId, loan.AccountNumber);
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "❌ [WORKER] Ошибка выполнения цикла Early Warning Worker.");
            }

            // Сканирование каждые 30 секунд
            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }
    }
}