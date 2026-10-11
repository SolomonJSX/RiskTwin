using Microsoft.EntityFrameworkCore;
using RiskTwin.Application.Interfaces;
using RiskTwin.Domain.Entities;
using RiskTwin.Domain.Enums;

namespace RiskTwin.Infrastructure.Persistence.Repositories;

public class UnitOfWork : IUnitOfWork
{
    private readonly RiskTwinDbContext _context;
    public UnitOfWork(RiskTwinDbContext context) => _context = context;
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) => _context.SaveChangesAsync(cancellationToken);
}

public class LoanRepository : ILoanRepository
{
    private readonly RiskTwinDbContext _context;
    public LoanRepository(RiskTwinDbContext context) => _context = context;

    public Task<Loan?> GetByIdAsync(Guid loanId, CancellationToken ct = default) =>
        _context.Loans.Include(l => l.Account).FirstOrDefaultAsync(l => l.LoanId == loanId, ct);

    public Task<List<Loan>> GetHighRiskLoansAsync(CancellationToken ct = default) =>
        _context.Loans
            .Include(l => l.ScoringEvents.OrderByDescending(s => s.TriggeredAt).Take(1))
            .Where(l => l.Status == "ACTIVE")
            .ToListAsync(ct);

    public Task UpdateAsync(Loan loan, CancellationToken ct = default)
    {
        _context.Loans.Update(loan);
        return Task.CompletedTask;
    }
}

public class RestructuringOfferRepository : IRestructuringOfferRepository
{
    private readonly RiskTwinDbContext _context;
    public RestructuringOfferRepository(RiskTwinDbContext context) => _context = context;

    public Task<List<RestructuringOffer>> GetActiveOffersByLoanIdAsync(Guid loanId, CancellationToken ct = default) =>
        _context.RestructuringOffers
            .Include(r => r.ScoringEvent)
            .Where(r => r.ScoringEvent.LoanId == loanId && r.Status == OfferStatus.Offered && r.ExpiresAt > DateTime.UtcNow)
            .ToListAsync(ct);

    public Task<RestructuringOffer?> GetByIdAsync(Guid offerId, CancellationToken ct = default) =>
        _context.RestructuringOffers
            .Include(r => r.ScoringEvent)
                .ThenInclude(s => s.Loan)
            .FirstOrDefaultAsync(r => r.OfferId == offerId, ct);

    public Task AddRangeAsync(IEnumerable<RestructuringOffer> offers, CancellationToken ct = default) =>
        _context.RestructuringOffers.AddRangeAsync(offers, ct);

    public Task UpdateAsync(RestructuringOffer offer, CancellationToken ct = default)
    {
        _context.RestructuringOffers.Update(offer);
        return Task.CompletedTask;
    }
}

public class ScoringEventRepository : IScoringEventRepository
{
    private readonly RiskTwinDbContext _context;
    public ScoringEventRepository(RiskTwinDbContext context) => _context = context;

    public async Task AddAsync(ScoringEvent scoringEvent, CancellationToken ct = default) =>
        await _context.ScoringEvents.AddAsync(scoringEvent, ct);
}