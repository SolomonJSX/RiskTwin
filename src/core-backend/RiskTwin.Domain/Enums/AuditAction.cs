namespace RiskTwin.Domain.Enums;

public enum AuditAction
{
    Generated,
    ViewedInApp,
    SignedOtp,
    RegulatorExport
}

public enum ActorType
{
    SystemOrTools,
    ClientDbo,
    RiskOfficer
}