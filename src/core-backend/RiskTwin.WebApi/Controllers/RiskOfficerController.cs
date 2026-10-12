using Microsoft.AspNetCore.Mvc;
using RiskTwin.Application.Interfaces;
using RiskTwin.Application.Services;

namespace RiskTwin.WebApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class RiskOfficerController : ControllerBase
{
    private readonly RestructuringWorkflowService _workflowService;
    private readonly ILoanRepository _loanRepo;

    public RiskOfficerController(RestructuringWorkflowService workflowService, ILoanRepository loanRepo)
    {
        _workflowService = workflowService;
        _loanRepo = loanRepo;
    }

    /// <summary>
    /// Получить портфель активных кредитов
    /// </summary>
    [HttpGet("loans")]
    public async Task<IActionResult> GetLoans(CancellationToken ct)
    {
        var loans = await _loanRepo.GetHighRiskLoansAsync(ct);
        return Ok(loans.Select(l => new
        {
            l.LoanId,
            l.ClientToken,
            l.AccountNumber,
            l.CurrentPrincipalBalance,
            l.MonthlyPayment,
            l.DaysPastDue,
            l.StageIfrs9,
            LastScoring = l.ScoringEvents.Select(s => new
            {
                s.EventId,
                s.PDefault30d,
                s.PDefault60d,
                s.TriggeredAt
            }).FirstOrDefault()
        }));
    }

    /// <summary>
    /// Запустить контур раннего предупреждения и генерацию планов реструктуризации
    /// </summary>
    [HttpPost("evaluate/{loanId:guid}")]
    public async Task<IActionResult> EvaluateLoan(
        Guid loanId,
        [FromQuery] decimal clientMonthlyIncome = 450000m,
        CancellationToken ct = default)
    {
        var eventId = await _workflowService.ProcessEarlyWarningAsync(loanId, clientMonthlyIncome, ct);
        return Ok(new
        {
            Success = true,
            ScoringEventId = eventId,
            Message = "Сквозной скоринг и оптимизация OR-Tools успешно выполнены"
        });
    }
}