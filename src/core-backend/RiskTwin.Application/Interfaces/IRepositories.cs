using RiskTwin.Domain.Entities;

namespace RiskTwin.Application.Interfaces;

public interface ILoanRepository
{
    Task<Loan?> GetByIdAsync(Guid loanId, CancellationToken cancellationToken = default);
    Task<List<Loan>> GetHighRiskLoansAsync(CancellationToken cancellationToken = default);
    Task UpdateAsync(Loan loan, CancellationToken cancellationToken = default);
}

public interface IRestructuringOfferRepository
{
    Task<List<RestructuringOffer>> GetActiveOffersByLoanIdAsync(Guid loanId, CancellationToken cancellationToken = default);
    Task<RestructuringOffer?> GetByIdAsync(Guid offerId, CancellationToken cancellationToken = default);
    Task AddRangeAsync(IEnumerable<RestructuringOffer> offers, CancellationToken cancellationToken = default);
    Task UpdateAsync(RestructuringOffer offer, CancellationToken cancellationToken = default);
}

public interface IScoringEventRepository
{
    Task AddAsync(ScoringEvent scoringEvent, CancellationToken cancellationToken = default);
}

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}