using RiskTwin.Application.Interfaces;
using Microsoft.Extensions.DependencyInjection;
using RiskTwin.Application.Services;

namespace RiskTwin.Application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<RestructuringWorkflowService>();
        services.AddScoped<IStalkerEngine, StalkerEngineService>();
        return services;
    }
}