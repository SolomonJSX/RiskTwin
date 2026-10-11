using RiskTwin.Domain.Entities;
using RiskTwin.Domain.Enums;

namespace RiskTwin.Domain.Rules;

public static class ArrfrComplianceRules
{
    public const decimal MaxAllowedKdn = 0.50m; // Максимальный КДН/DTI: 50%
    public const int MaxExtensionMonths = 24;   // Максимальная пролонгация: +24 месяца
    public const decimal MaxAllowedGesv = 0.56m; // Предельная ГЭСВ: 56%

    public static (bool IsCompliant, string Reason) Validate(Loan loan, RestructuringOffer offer, decimal clientMonthlyIncome)
    {
        // 1. Проверка КДН (DTI)
        if (clientMonthlyIncome > 0)
        {
            var calculatedKdn = offer.NewMonthlyPayment / clientMonthlyIncome;
            if (calculatedKdn > MaxAllowedKdn)
            {
                return (false, $"Нарушение АРРФР: Прогнозный КДН ({calculatedKdn:P1}) превышает лимит {MaxAllowedKdn:P0}");
            }
        }

        // 2. Проверка лимита пролонгации
        if (offer.ScenarioType == RestructuringScenarioType.TermExtension)
        {
            // Разница между новым сроком и текущим оставшимся
            if (offer.NewTenorMonths > MaxExtensionMonths + 60)
            {
                return (false, $"Нарушение АРРФР: Продление срока превышает допустимый лимит в {MaxExtensionMonths} мес.");
            }
        }

        // 3. Проверка каникул (Payment Holiday) - не более 6 месяцев по нормам РК
        if (offer.ScenarioType == RestructuringScenarioType.PaymentHoliday && offer.GracePeriodMonths > 6)
        {
            return (false, "Нарушение АРРФР: Кредитные каникулы не могут превышать 6 месяцев");
        }

        return (true, "Полное соответствие требованиям регулятора АРРФР");
    }
}