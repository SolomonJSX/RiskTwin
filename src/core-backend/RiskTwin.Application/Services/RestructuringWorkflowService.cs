using System.Text.Json;
using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using RiskTwin.Domain.Entities;
using RiskTwin.Domain.Enums;
using RiskTwin.Domain.Rules;

namespace RiskTwin.Application.Services;

public class RestructuringWorkflowService
{
    private readonly IMlInferenceClient _mlClient;
    private readonly IFeatureStore _featureStore;
    private readonly ILoanRepository _loanRepo;
    private readonly IScoringEventRepository _scoringRepo;
    private readonly IRestructuringOfferRepository _offerRepo;
    private readonly IAuditService _auditService;
    private readonly IUnitOfWork _unitOfWork;

    public RestructuringWorkflowService(
        IMlInferenceClient mlClient,
        IFeatureStore featureStore,
        ILoanRepository loanRepo,
        IScoringEventRepository scoringRepo,
        IRestructuringOfferRepository offerRepo,
        IAuditService auditService,
        IUnitOfWork unitOfWork)
    {
        _mlClient = mlClient;
        _featureStore = featureStore;
        _loanRepo = loanRepo;
        _scoringRepo = scoringRepo;
        _offerRepo = offerRepo;
        _auditService = auditService;
        _unitOfWork = unitOfWork;
    }

    /// <summary>
    /// Запуск цикла оценки и генерации офферов (Раннее предупреждение)
    /// </summary>
    public async Task<Guid?> ProcessEarlyWarningAsync(Guid loanId, decimal clientMonthlyIncome, CancellationToken ct = default)
    {
        var loan = await _loanRepo.GetByIdAsync(loanId, ct);
        if (loan == null)
        {
            var loans = await _loanRepo.GetHighRiskLoansAsync(ct);
            loan = loans.FirstOrDefault();
        }
        if (loan == null) throw new InvalidOperationException($"Кредит {loanId} не найден");

        // 1. Получаем скользящие окна из Feature Store (Redis)
        var features = await _featureStore.GetFeaturesAsync(loan.ClientToken, ct);

        // 2. Готовим параметры кредита для оптимизатора OR-Tools
        var loanDetails = new LoanDetailsDto(
            RemainingPrincipal: loan.CurrentPrincipalBalance,
            InterestRate: loan.InterestRate,
            RemainingTermMonths: Math.Max(1, (loan.MaturityDate.Year - DateTime.UtcNow.Year) * 12 + loan.MaturityDate.Month - DateTime.UtcNow.Month),
            CurrentMonthlyPayment: loan.MonthlyPayment,
            EstimatedCapacity: clientMonthlyIncome * 0.40m // емкость клиента (до 40% от дохода)
        );

        // 3. Вызов Python ML Engine (gRPC)
        var analysis = await _mlClient.EvaluateAndOptimizeAsync(loan.ClientToken, loanDetails, features, ct);

        // 4. Фиксируем Scoring Event в PostgreSQL
        var scoringEvent = new ScoringEvent
        {
            LoanId = loan.LoanId,
            PDefault30d = analysis.PDefault30d,
            PDefault60d = analysis.PDefault60d,
            ModelVersion = "LightGBM_Survival_v1",
            ShapFactorsJson = JsonSerializer.Serialize(analysis.TopRiskDrivers),
            FeatureSnapshotJson = JsonSerializer.Serialize(features),
            TriggeredAt = DateTime.UtcNow
        };
        await _scoringRepo.AddAsync(scoringEvent, ct);

        // 5. Если риск высокий - валидируем сценарии по правилам АРРФР и создаем офферы
        if (analysis.IsHighRisk && analysis.Scenarios.Any())
        {
            var validOffers = new List<RestructuringOffer>();

            foreach (var sc in analysis.Scenarios)
            {
                var offer = new RestructuringOffer
                {
                    EventId = scoringEvent.EventId,
                    ScenarioType = sc.ScenarioType,
                    NewTenorMonths = sc.NewTenorMonths,
                    NewMonthlyPayment = sc.NewMonthlyPayment,
                    GracePeriodMonths = sc.GracePeriodMonths,
                    NpvRecoveryEst = sc.NpvRecoveryEst,
                    KdnPostRestructure = clientMonthlyIncome > 0 ? (sc.NewMonthlyPayment / clientMonthlyIncome) : 0,
                    Status = OfferStatus.Offered,
                    ExpiresAt = DateTime.UtcNow.AddDays(14) // Оффер действует 14 дней в ДБО
                };

                // Проверка регуляторного комплаенса АРРФР
                var (isCompliant, reason) = ArrfrComplianceRules.Validate(loan, offer, clientMonthlyIncome);
                if (isCompliant)
                {
                    validOffers.Add(offer);
                }
            }

            if (validOffers.Any())
            {
                await _offerRepo.AddRangeAsync(validOffers, ct);
            }
        }

        await _unitOfWork.SaveChangesAsync(ct);

        // 6. Аудит события для проверок регулятора
        await _auditService.LogAsync(
            loanId: loan.LoanId,
            offerId: null,
            action: AuditAction.Generated,
            actorType: ActorType.SystemOrTools,
            actorId: "Saga_Orchestrator",
            payload: new { analysis.PDefault30d, analysis.IsHighRisk, ScenariosCount = analysis.Scenarios.Count },
            cancellationToken: ct
        );

        return scoringEvent.EventId;
    }

    /// <summary>
    /// Смарт-подписание оффера клиентом в Мобильном ДБО (SMS-OTP / ЭЦП)
    /// </summary>
    public async Task<bool> SignOfferByClientAsync(Guid offerId, string otpCode, CancellationToken ct = default)
    {
        var offer = await _offerRepo.GetByIdAsync(offerId, ct);
        if (offer == null || offer.Status != OfferStatus.Offered) return false;

        // Эмуляция проверки OTP
        if (otpCode != "7777") return false;

        offer.Status = OfferStatus.Accepted;
        offer.SignedAt = DateTime.UtcNow;
        await _offerRepo.UpdateAsync(offer, ct);

        // Обновляем параметры самого кредита
        var loan = await _loanRepo.GetByIdAsync(offer.ScoringEvent.LoanId, ct);
        if (loan != null)
        {
            loan.MonthlyPayment = offer.NewMonthlyPayment;
            loan.UpdatedAt = DateTime.UtcNow;
            await _loanRepo.UpdateAsync(loan, ct);
        }

        await _unitOfWork.SaveChangesAsync(ct);

        // Аудит подписания
        await _auditService.LogAsync(
            loanId: loan!.LoanId,
            offerId: offer.OfferId,
            action: AuditAction.SignedOtp,
            actorType: ActorType.ClientDbo,
            actorId: $"Client_{offer.ScoringEvent.Loan.ClientToken}",
            payload: new { offer.ScenarioType, offer.NewMonthlyPayment, SignedAt = offer.SignedAt },
            cancellationToken: ct
        );

        return true;
    }
}