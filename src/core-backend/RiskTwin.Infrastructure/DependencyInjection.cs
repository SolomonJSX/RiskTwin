using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using RiskTwin.Application.Interfaces;
using RiskTwin.Infrastructure.GrpcClients;
using RiskTwin.Infrastructure.Persistence;
using RiskTwin.Infrastructure.Persistence.Repositories;
using RiskTwin.Infrastructure.Services;

namespace RiskTwin.Infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        var connectionString = configuration.GetConnectionString("DefaultConnection") 
    ?? "Host=localhost;Port=5433;Database=risktwin_db;Username=risktwin_user;Password=risktwin_password";

        services.AddDbContext<RiskTwinDbContext>(options =>
            options.UseNpgsql(connectionString));

        services.AddScoped<IUnitOfWork, UnitOfWork>();
        services.AddScoped<ILoanRepository, LoanRepository>();
        services.AddScoped<IRestructuringOfferRepository, RestructuringOfferRepository>();
        services.AddScoped<IScoringEventRepository, ScoringEventRepository>();
        services.AddScoped<IStalkerRepository, StalkerRepository>();

        services.AddScoped<IAuditService, Sha256AuditService>();

        // Настройка Redis Feature Store
        var redisConnString = configuration.GetConnectionString("Redis") ?? "localhost:6379";
        services.AddSingleton<StackExchange.Redis.IConnectionMultiplexer>(_ => 
        {
            try
            {
                var options = StackExchange.Redis.ConfigurationOptions.Parse(redisConnString);
                options.AbortOnConnectFail = false;
                options.ConnectTimeout = 2000;
                return StackExchange.Redis.ConnectionMultiplexer.Connect(options);
            }
            catch
            {
                return null!;
            }
        });
        services.AddScoped<IFeatureStore, RedisFeatureStore>();

        var grpcUrl = configuration["GrpcSettings:MlInferenceUrl"] ?? "http://localhost:50051";
        services.AddSingleton<IMlInferenceClient>(_ => new MlInferenceGrpcClient(grpcUrl));

        return services;
    }
}