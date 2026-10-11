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

builder.Services.AddControllers();
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

    // Сидируем тестового клиента, если база пустая
    if (!await db.Accounts.AnyAsync())
    {
        var testClientToken = Guid.Parse("11111111-2222-3333-4444-555555555555");
        var testLoanId = Guid.Parse("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");

        var account = new Account
        {
            ClientToken = testClientToken,
            Segment = "MASS",
            CurrentKdn = 0.58m,
            IsRestructuringActive = false
        };

        var loan = new Loan
        {
            LoanId = testLoanId,
            ClientToken = testClientToken,
            AccountNumber = "KZ886010002003004005",
            OriginalPrincipal = 2_500_000m,
            CurrentPrincipalBalance = 1_850_000m,
            InterestRate = 0.22m,
            EffectiveRateGesv = 0.245m,
            MonthlyPayment = 78_500m,
            MaturityDate = DateOnly.FromDateTime(DateTime.UtcNow.AddMonths(36)),
            DaysPastDue = 3,
            StageIfrs9 = "STAGE_1",
            Status = "ACTIVE"
        };

        db.Accounts.Add(account);
        db.Loans.Add(loan);
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