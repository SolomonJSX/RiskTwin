using Microsoft.EntityFrameworkCore;
using RiskTwin.Application;
using RiskTwin.Domain.Entities;
using RiskTwin.Infrastructure;
using RiskTwin.Infrastructure.Persistence;
using RiskTwin.WebApi;

var builder = WebApplication.CreateBuilder(args);

// Подключаем слои Clean Architecture
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
        policy.WithOrigins("http://localhost:5173", "http://localhost:3000")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

builder.Services.AddSignalR();

var app = builder.Build();

// Автоматическое применение схемы БД и сидирование демо-данных
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<RiskTwinDbContext>();
    await db.Database.EnsureCreatedAsync();

    // Наполняем портфель активных заемщиков для красивой и разнообразной демонстрации
    if (await db.Loans.CountAsync() <= 1)
    {
        var sampleLoans = new List<(string Name, decimal Principal, decimal Monthly, int Dpd, string Stage, decimal Kdn, float Pd)>
        {
            ("KZ886010002003004001", 3_200_000m, 92_000m, 5, "STAGE_2", 0.62m, 0.78f),
            ("KZ886010002003004002", 1_450_000m, 48_500m, 0, "STAGE_1", 0.38m, 0.12f),
            ("KZ886010002003004003", 5_800_000m, 165_000m, 12, "STAGE_2", 0.71m, 0.85f),
            ("KZ886010002003004004", 890_000m, 31_200m, 0, "STAGE_1", 0.29m, 0.08f),
            ("KZ886010002003004005", 2_100_000m, 74_000m, 2, "STAGE_1", 0.54m, 0.45f),
            ("KZ886010002003004006", 4_300_000m, 128_000m, 18, "STAGE_2", 0.68m, 0.82f),
            ("KZ886010002003004007", 1_750_000m, 56_000m, 0, "STAGE_1", 0.35m, 0.14f),
            ("KZ886010002003004008", 6_500_000m, 190_000m, 7, "STAGE_2", 0.75m, 0.91f),
            ("KZ886010002003004009", 950_000m, 34_000m, 0, "STAGE_1", 0.31m, 0.11f),
            ("KZ886010002003004010", 3_800_000m, 115_000m, 4, "STAGE_1", 0.59m, 0.52f),
        };

        foreach (var (accNum, principal, monthly, dpd, stage, kdn, pd) in sampleLoans)
        {
            var cToken = Guid.NewGuid();
            var lId = Guid.NewGuid();

            var acc = new Account
            {
                ClientToken = cToken,
                Segment = "MASS",
                CurrentKdn = kdn,
                IsRestructuringActive = false
            };

            var ln = new Loan
            {
                LoanId = lId,
                ClientToken = cToken,
                AccountNumber = accNum,
                OriginalPrincipal = principal * 1.2m,
                CurrentPrincipalBalance = principal,
                InterestRate = 0.21m,
                EffectiveRateGesv = 0.235m,
                MonthlyPayment = monthly,
                MaturityDate = DateOnly.FromDateTime(DateTime.UtcNow.AddMonths(24)),
                DaysPastDue = dpd,
                StageIfrs9 = stage,
                Status = "ACTIVE"
            };

            var sc = new ScoringEvent
            {
                EventId = Guid.NewGuid(),
                LoanId = lId,
                PDefault30d = pd,
                PDefault60d = Math.Min(pd * 1.15f, 0.99f),
                ModelVersion = "LightGBM_v2",
                TriggeredAt = DateTime.UtcNow.AddMinutes(-new Random().Next(10, 240))
            };

            db.Accounts.Add(acc);
            db.Loans.Add(ln);
            db.ScoringEvents.Add(sc);
        }

        await db.SaveChangesAsync();
    }

    // Сидируем 1000 заемщиков Сталкера из сгенерированного CSV
    var baseDir = Path.GetFullPath(Path.Combine(app.Environment.ContentRootPath, "..", ".."));
    var csvPath = Path.Combine(baseDir, "ml-engine", "training", "credit_behavior_dataset.csv");
    await db.SeedClientProfilesFromCsvAsync(csvPath);
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