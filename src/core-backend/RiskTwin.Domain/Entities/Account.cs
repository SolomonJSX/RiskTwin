namespace RiskTwin.Domain.Entities;

public class Account
{
    public Guid ClientToken { get; set; }
    public string Segment { get; set; } = "MASS";
    public decimal CurrentKdn { get; set; } // КДН (Коэффициент долговой нагрузки)
    public bool IsRestructuringActive { get; set; } = false;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public List<Loan> Loans { get; set; } = new();
}