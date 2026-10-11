import torch
import torch.nn as nn
import torch.nn.functional as F


class BiTemporalGRUSequenceEncoder(nn.Module):
    """
    Последовательный энкодер на базе двунаправленного GRU (Bi-GRU).
    Кодирует 30-дневные временные ряды расходов/балансов заемщика:
    Вход:  [Batch, seq_len=30, input_dim=3] (например, [ежедневные траты, баланс счета, число сессий ДБО])
    Выход: [Batch, embed_dim] вектор динамического тренда стресса заемщика.
    """

    def __init__(self, input_dim: int = 3, hidden_dim: int = 32, embed_dim: int = 32, num_layers: int = 2):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.15 if num_layers > 1 else 0.0,
        )
        self.proj = nn.Sequential(
            nn.Linear(hidden_dim * 2, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.GELU(),
        )

    def forward(self, x_seq: torch.Tensor) -> torch.Tensor:
        # x_seq: [Batch, 30, input_dim]
        gru_out, _ = self.gru(x_seq)  # [Batch, 30, hidden_dim * 2]
        # Берем последнее скрытое состояние во времени или mean pooling
        temporal_pooled = torch.mean(gru_out, dim=1)  # [Batch, hidden_dim * 2]
        return self.proj(temporal_pooled)            # [Batch, embed_dim]
