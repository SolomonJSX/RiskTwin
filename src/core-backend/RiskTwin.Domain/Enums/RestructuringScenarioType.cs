namespace RiskTwin.Domain.Enums;

public enum RestructuringScenarioType
{
    PaymentHoliday = 1,   // Кредитные каникулы (полная отсрочка)
    TermExtension = 2,    // Пролонгация срока со снижением платежа
    GracePeriod = 3       // Грейс-период (выплата только % без тела)
}