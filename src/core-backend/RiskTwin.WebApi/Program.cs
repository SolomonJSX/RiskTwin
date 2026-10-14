using Microsoft.EntityFrameworkCore;
using RiskTwin.Application;
using RiskTwin.Domain.Entities;
using RiskTwin.Infrastructure;
using RiskTwin.Infrastructure.Persistence;
using RiskTwin.WebApi;

var builder = WebApplication.CreateBuilder(args);

// Сервисы Clean Architecture
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.ReferenceHandler = System.Text.Json.Serialization.ReferenceHandler.IgnoreCycles;
    });
builder.Services.AddHostedService<EarlyWarningBackgroundWorker>();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.WithOrigins("http://localhost:5173", "http://localhost:3000", "http://localhost:8001")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

builder.Services.AddSignalR();

var app = builder.Build();

// Автоматическая синхронизация схемы БД и единого фокусного двойника Армана
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<RiskTwinDbContext>();
    await db.Database.EnsureCreatedAsync();

    var armanClientToken = Guid.Parse("11111111-2222-3333-4444-555555555555");
    var armanLoanId = Guid.Parse("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");
    var armanAccountNum = "KZ886010002003004001";

    // 1. Очищаем устаревшие тестовые кредиты через безопасный SQL порядок с сохранением внешних ключей
    await db.Database.ExecuteSqlRawAsync(@"
        INSERT INTO accounts (client_token, segment, current_kdn, is_restructuring_active, created_at)
        VALUES ('11111111-2222-3333-4444-555555555555', 'IT-Сеньор', 0.12, false, NOW())
        ON CONFLICT (client_token) DO NOTHING;

        UPDATE loans SET client_token = '11111111-2222-3333-4444-555555555555' WHERE account_number = 'KZ886010002003004001';

        DELETE FROM restructuring_offers WHERE event_id IN (
            SELECT event_id FROM scoring_events WHERE loan_id NOT IN (
                SELECT loan_id FROM loans WHERE account_number = 'KZ886010002003004001'
            )
        );
        DELETE FROM scoring_events WHERE loan_id NOT IN (SELECT loan_id FROM loans WHERE account_number = 'KZ886010002003004001');

        DELETE FROM loans WHERE account_number <> 'KZ886010002003004001';
        DELETE FROM accounts WHERE client_token <> '11111111-2222-3333-4444-555555555555';

        UPDATE loans SET 
            current_principal_balance = 4200000, 
            original_principal = 4830000, 
            monthly_payment = 145000, 
            days_past_due = 0, 
            stage_ifrs9 = 'STAGE_1', 
            status = 'ACTIVE' 
        WHERE account_number = 'KZ886010002003004001';

        UPDATE scoring_events SET 
            p_default_30d = 0.013, 
            p_default_60d = 0.015, 
            model_version = 'PyTorch_DualTower_360_v3' 
        WHERE loan_id IN (SELECT loan_id FROM loans WHERE account_number = 'KZ886010002003004001');
    ");

    // 2. Если кредита Армана не было, создаем его
    if (!await db.Loans.AnyAsync(l => l.AccountNumber == armanAccountNum))
    {
        var loan = new Loan
        {
            LoanId = armanLoanId,
            ClientToken = armanClientToken,
            AccountNumber = armanAccountNum,
            OriginalPrincipal = 4830000m,
            CurrentPrincipalBalance = 4200000m,
            InterestRate = 0.21m,
            EffectiveRateGesv = 0.235m,
            MonthlyPayment = 145000m,
            MaturityDate = DateOnly.FromDateTime(DateTime.UtcNow.AddMonths(24)),
            DaysPastDue = 0,
            StageIfrs9 = "STAGE_1",
            Status = "ACTIVE"
        };
        db.Loans.Add(loan);
        await db.SaveChangesAsync();

        var scoring = new ScoringEvent
        {
            EventId = Guid.NewGuid(),
            LoanId = armanLoanId,
            PDefault30d = 0.013f,
            PDefault60d = 0.015f,
            ModelVersion = "PyTorch_DualTower_360_v3",
            TriggeredAt = DateTime.UtcNow
        };
        db.ScoringEvents.Add(scoring);
        await db.SaveChangesAsync();
    }
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("AllowAll");
app.UseAuthorization();
app.MapControllers();
app.MapHub<RiskTwin.WebApi.Hubs.StalkerHub>("/hubs/stalker");

app.Run();