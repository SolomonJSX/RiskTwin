using Microsoft.AspNetCore.Mvc;
using RiskTwin.Application.Interfaces;
using RiskTwin.Application.Services;

namespace RiskTwin.WebApi.Controllers;

public record SignOfferRequest(Guid OfferId, string OtpCode);

[ApiController]
[Route("api/[controller]")]
public class DboClientController : ControllerBase
{
    private readonly RestructuringWorkflowService _workflowService;
    private readonly IRestructuringOfferRepository _offerRepo;

    public DboClientController(RestructuringWorkflowService workflowService, IRestructuringOfferRepository offerRepo)
    {
        _workflowService = workflowService;
        _offerRepo = offerRepo;
    }

    /// <summary>
    /// Получить 3 персонализированных сценария реструктуризации для клиента
    /// </summary>
    [HttpGet("offers/{loanId:guid}")]
    public async Task<IActionResult> GetActiveOffers(Guid loanId, CancellationToken ct)
    {
        var offers = await _offerRepo.GetActiveOffersByLoanIdAsync(loanId, ct);
        return Ok(offers.Select(o => new
        {
            o.OfferId,
            ScenarioType = o.ScenarioType.ToString(),
            o.NewTenorMonths,
            o.NewMonthlyPayment,
            o.GracePeriodMonths,
            NpvRecoveryRate = o.NpvRecoveryEst,
            o.KdnPostRestructure,
            o.Status,
            o.ExpiresAt
        }));
    }

    /// <summary>
    /// Смарт-подписание оффера клиентом (SMS-OTP: тестовый код 7777)
    /// </summary>
    [HttpPost("sign")]
    public async Task<IActionResult> SignOffer([FromBody] SignOfferRequest request, CancellationToken ct)
    {
        var success = await _workflowService.SignOfferByClientAsync(request.OfferId, request.OtpCode, ct);
        if (!success)
        {
            return BadRequest(new { Success = false, Message = "Неверный OTP код либо оффер недоступен для подписания" });
        }

        return Ok(new
        {
            Success = true,
            Message = "Соглашение о реструктуризации успешно подписано и зарегистрировано в регуляторном аудите АРРФР"
        });
    }
}