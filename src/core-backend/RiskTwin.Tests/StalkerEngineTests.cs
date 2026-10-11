using FluentAssertions;
using Microsoft.EntityFrameworkCore;
using Moq;
using RiskTwin.Application.DTOs;
using RiskTwin.Application.Interfaces;
using RiskTwin.Application.Services;
using RiskTwin.Domain.Entities;
using RiskTwin.Infrastructure.Persistence;
using RiskTwin.Infrastructure.Persistence.Repositories;
using Xunit;

namespace RiskTwin.Tests;

public class StalkerEngineTests
{
    private readonly RiskTwinDbContext _dbContext;
    private readonly StalkerRepository _stalkerRepo;
    private readonly Mock<IMlInferenceClient> _mockMlClient;
    private readonly Mock<IFeatureStore> _mockFeatureStore;
    private readonly StalkerEngineService _stalkerEngine;

    public StalkerEngineTests()
    {
        // Изолированная база данных в памяти (In-Memory DB) для чистоты каждого теста
        var options = new DbContextOptionsBuilder<RiskTwinDbContext>()
            .UseInMemoryDatabase(databaseName: $"StalkerTestDb_{Guid.NewGuid()}")
            .Options;

        _dbContext = new RiskTwinDbContext(options);
        _stalkerRepo = new StalkerRepository(_dbContext);
        _mockMlClient = new Mock<IMlInferenceClient>();
        _mockFeatureStore = new Mock<IFeatureStore>();

        _stalkerEngine = new StalkerEngineService(
            _stalkerRepo,
            _mockMlClient.Object,
            _mockFeatureStore.Object);
    }

    private async Task<ClientProfile> SeedSampleClientAsync(
        string token = "test-token-001",
        double initialRisk = 0.12,
        string archetype = "STABLE")
    {
        var profile = new ClientProfile
        {
            ClientToken = token,
            FullName = "Сатпаев Арман Кайратович",
            Iin = "851112370188",
            City = "Алматы",
            Age = 41,
            DeclaredIncome = 650000m,
            Archetype = archetype,
            CurrentRiskScore = initialRisk,
            RiskLevel = initialRisk >= 0.60 ? "RED" : (initialRisk >= 0.35 ? "YELLOW" : "GREEN"),
            IsUnderStalkerWatch = true,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow
        };

        await _dbContext.ClientProfiles.AddAsync(profile);
        await _dbContext.SaveChangesAsync();
        return profile;
    }

    // ==============================================================================
    // ТЕСТ 1: Перевод в МФО должен мгновенно вызывать CRITICAL-алерт и рост риска
    // ==============================================================================
    [Fact]
    public async Task ProcessTelemetryEvent_WhenMfoTransfer_ShouldTriggerCriticalAlertWithHighDelta()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.15);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.MfoTransfer,
            Amount: 50000m,
            MerchantOrRecipient: "Займер KZ"
        );

        // Act
        var result = await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);

        // Assert
        result.AlertTriggered.Should().BeTrue();
        result.Severity.Should().Be("CRITICAL");
        result.TriggerType.Should().Be("MFO_TRANSFER");
        result.DeltaRisk.Should().BeGreaterThanOrEqualTo(0.40);
        result.NewRisk.Should().BeGreaterThan(0.55);

        // Проверка двуязычного объяснения
        result.ReasonRu.Should().Contain("Займер KZ").And.Contain("МФО").And.Contain("долговой спирали");
        result.ReasonKz.Should().Contain("МҚҰ").And.Contain("қаупі");
        result.RecommendedAction.Should().Contain("Кредитные каникулы");

        // Проверка сохранения алерта в БД
        var savedAlert = await _dbContext.StalkerAlerts.FirstOrDefaultAsync(a => a.ClientToken == client.ClientToken);
        savedAlert.Should().NotBeNull();
        savedAlert!.Severity.Should().Be("CRITICAL");
    }

    // ==============================================================================
    // ТЕСТ 2: Задержка зарплаты на 12 дней должна маркироваться критической
    // ==============================================================================
    [Fact]
    public async Task ProcessTelemetryEvent_WhenSevereSalaryDelay_ShouldEscalateSeverity()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.20);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.SalaryDelay,
            DelayDays: 12
        );

        // Act
        var result = await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);

        // Assert
        result.AlertTriggered.Should().BeTrue();
        result.Severity.Should().Be("CRITICAL");
        result.TriggerType.Should().Be("SALARY_DELAY");
        result.ReasonRu.Should().Contain("12 дней");
        result.RecommendedAction.Should().Contain("перенос даты");
    }

    // ==============================================================================
    // ТЕСТ 3: Падение зарплаты (INCOME_SHOCK) со снижением более 30%
    // ==============================================================================
    [Fact]
    public async Task ProcessTelemetryEvent_WhenIncomeShock_ShouldSuggestTermExtension()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.10);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.SalaryCut,
            SalaryDropPercent: 35.0
        );

        // Act
        var result = await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);

        // Assert
        result.AlertTriggered.Should().BeTrue();
        result.TriggerType.Should().Be("INCOME_SHOCK");
        result.DeltaRisk.Should().BeGreaterThan(0.30);
        result.RecommendedAction.Should().Contain("Пролонгация");
    }

    // ==============================================================================
    // ТЕСТ 4: Каскад рассрочек BNPL (Kaspi/Halyk 0-0-24)
    // ==============================================================================
    [Fact]
    public async Task ProcessTelemetryEvent_WhenBnplSurge_ShouldTriggerOverleveragedAlert()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.25);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.BnplSurge,
            NewBnplCount: 6
        );

        // Act
        var result = await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);

        // Assert
        result.AlertTriggered.Should().BeTrue();
        result.TriggerType.Should().Be("BNPL_OVERLEVERAGED");
        result.ReasonRu.Should().Contain("6-й");
        result.RecommendedAction.Should().Contain("Консолидация");
    }

    // ==============================================================================
    // ТЕСТ 5: Хронологическая шкала (Timeline Snapshot) должна фиксировать дельту
    // ==============================================================================
    [Fact]
    public async Task ProcessTelemetryEvent_ShouldCreateTimelineSnapshotWithAccurateDelta()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.10);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.DboNightAnxiety
        );

        // Act
        await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);

        // Assert
        var timeline = await _stalkerEngine.GetClientTimelineAsync(client.ClientToken);
        timeline.Should().HaveCount(1);
        timeline[0].DeltaPd.Should().BeGreaterThan(0);
        timeline[0].RiskScore.Should().BeApproximately(0.25, 0.05);
        timeline[0].EventDescriptionRu.Should().Contain("ночных входа");
    }

    // ==============================================================================
    // ТЕСТ 6: Подтверждение реакции риск-офицера (Acknowledge)
    // ==============================================================================
    [Fact]
    public async Task AcknowledgeAlert_ShouldSetOfficerNameAndTimestamp()
    {
        // Arrange
        var client = await SeedSampleClientAsync(initialRisk: 0.20);
        var telemetry = new StalkerTelemetryEventDto(
            ClientToken: client.ClientToken,
            EventType: StalkerEventType.MfoTransfer,
            Amount: 30000m
        );
        var analysis = await _stalkerEngine.ProcessTelemetryEventAsync(telemetry);
        analysis.AlertId.Should().NotBeNull();

        // Act
        var acknowledged = await _stalkerEngine.AcknowledgeAlertAsync(
            analysis.AlertId!.Value,
            officerName: "Офицер-Аналитик Ерлан",
            notes: "Связался с клиентом, направлен оффер каникул"
        );

        // Assert
        acknowledged.Should().BeTrue();
        var alertInDb = await _dbContext.StalkerAlerts.FindAsync(analysis.AlertId!.Value);
        alertInDb.Should().NotBeNull();
        alertInDb!.IsAcknowledged.Should().BeTrue();
        alertInDb.AcknowledgedBy.Should().Be("Офицер-Аналитик Ерлан");
        alertInDb.AcknowledgedAt.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(5));
    }
}