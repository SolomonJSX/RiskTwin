import torch
import torch.nn as nn
import torch.nn.functional as F


class FeatureTokenizer(nn.Module):
    """
    Feature Tokenizer (FT-Transformer approach):
    Преобразует каждый отдельный числовой признак x_i в вектор-токен размерности d:
    e_i = x_i * W_i + b_i.
    Результат: тензор [Batch, num_features, embed_dim].
    """

    def __init__(self, num_features: int, embed_dim: int):
        super().__init__()
        self.num_features = num_features
        self.embed_dim = embed_dim
        # Веса проекции для каждого признака отдельно
        self.weight = nn.Parameter(torch.randn(num_features, embed_dim) * 0.02)
        self.bias = nn.Parameter(torch.zeros(num_features, embed_dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [Batch, num_features]
        # x.unsqueeze(-1): [Batch, num_features, 1]
        # self.weight.unsqueeze(0): [1, num_features, embed_dim]
        # Результат: [Batch, num_features, embed_dim]
        tokens = x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)
        return tokens


class DualTowerCrossAttentionNet(nn.Module):
    """
    Глубокая двухбашенная нейросеть с Feature Tokenizer и честным Multi-Head Cross-Attention.
    
    Архитектура:
    - Башня 1 (Финансы): 7 признаков -> FeatureTokenizer -> [Batch, 7, embed_dim]
    - Башня 2 (Психология): 9 признаков -> FeatureTokenizer -> [Batch, 9, embed_dim]
    - Cross-Attention:
        Query: 7 финансовых токенов
        Key/Value: 9 психологических токенов
        Внимание: [Batch, 7, 9] - физически осмысленная матрица синергии каждого финансового
                  стресс-маркера с каждым психоэмоциональным фактором.
    - Multi-Task Learning (MTL):
        1. Вероятность дефолта (P_Default, классификация)
        2. Дней до наступления дефолта (Survival Days, регрессия)
    """

    def __init__(
        self,
        fin_dim: int = 7,
        psycho_dim: int = 9,
        embed_dim: int = 32,
        num_heads: int = 4,
        dropout: float = 0.15,
    ):
        super().__init__()
        self.fin_dim = fin_dim
        self.psycho_dim = psycho_dim
        self.embed_dim = embed_dim

        # 1. Feature Tokenizers
        self.fin_tokenizer = FeatureTokenizer(fin_dim, embed_dim)
        self.psycho_tokenizer = FeatureTokenizer(psycho_dim, embed_dim)

        self.fin_norm = nn.LayerNorm(embed_dim)
        self.psycho_norm = nn.LayerNorm(embed_dim)

        # 2. Self-Attention блоки внутри каждого домена
        self.fin_self_attn = nn.MultiheadAttention(
            embed_dim=embed_dim, num_heads=num_heads, dropout=dropout, batch_first=True
        )
        self.psycho_self_attn = nn.MultiheadAttention(
            embed_dim=embed_dim, num_heads=num_heads, dropout=dropout, batch_first=True
        )

        # 3. Кросс-внимание: Финансовые токены обогащаются психологическими контекстами
        # Query: [Batch, 7, embed_dim], Key/Value: [Batch, 9, embed_dim]
        self.cross_attention = nn.MultiheadAttention(
            embed_dim=embed_dim, num_heads=num_heads, dropout=dropout, batch_first=True
        )
        self.cross_norm = nn.LayerNorm(embed_dim)

        # 4. Pooling и Fusion
        # 7 токенов финансов + 9 токенов психологии + 7 токенов кросс-внимания + temporal_token (embed_dim)
        total_dim = (fin_dim + psycho_dim + fin_dim + 1) * embed_dim  # (7 + 9 + 7 + 1) * 32 = 768
        self.temporal_encoder = nn.GRU(
            input_size=3, hidden_size=embed_dim // 2, batch_first=True, bidirectional=True
        )
        self.temporal_proj = nn.Linear(embed_dim, embed_dim)

        self.fusion = nn.Sequential(
            nn.Linear(total_dim, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, 64),
            nn.LayerNorm(64),
            nn.GELU(),
            nn.Dropout(dropout),
        )

        # 5. Multi-Task Heads
        self.default_head = nn.Linear(64, 1)
        self.survival_head = nn.Sequential(
            nn.Linear(64, 1),
            nn.Softplus(),
        )

    def forward(
        self,
        fin_x: torch.Tensor,
        psycho_x: torch.Tensor,
        seq_x: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # 1. Токенизация числовых признаков
        fin_tokens = self.fin_norm(self.fin_tokenizer(fin_x))          # [Batch, 7, embed_dim]
        psycho_tokens = self.psycho_norm(self.psycho_tokenizer(psycho_x)) # [Batch, 9, embed_dim]

        # 2. Внутридоменное самовнимание (Self-Attention)
        fin_self, _ = self.fin_self_attn(fin_tokens, fin_tokens, fin_tokens)
        fin_tokens = fin_tokens + fin_self

        psycho_self, _ = self.psycho_self_attn(psycho_tokens, psycho_tokens, psycho_tokens)
        psycho_tokens = psycho_tokens + psycho_self

        # 3. Честное Кросс-внимание (Cross-Attention [Batch, 7, 9])
        # Финансы опрашивают психологический кризис
        cross_out, attn_weights = self.cross_attention(
            query=fin_tokens,
            key=psycho_tokens,
            value=psycho_tokens,
        )
        cross_tokens = self.cross_norm(fin_tokens + cross_out)  # [Batch, 7, embed_dim]

        # 4. Временной последовательный анализ (30-дневная динамика транзакций)
        b_size = fin_x.size(0)
        if seq_x is not None:
            t_out, _ = self.temporal_encoder(seq_x)
            temporal_vec = self.temporal_proj(t_out.mean(dim=1))
        else:
            # Создаем нейтральный синтетический эмбеддинг временного ряда из fin_x
            temporal_vec = torch.zeros(b_size, self.embed_dim, device=fin_x.device)

        # 5. Слияние представлений
        flat_fin = fin_tokens.reshape(b_size, -1)
        flat_psycho = psycho_tokens.reshape(b_size, -1)
        flat_cross = cross_tokens.reshape(b_size, -1)

        combined = torch.cat([flat_fin, flat_psycho, flat_cross, temporal_vec], dim=-1)
        latent = self.fusion(combined)

        # 6. Выходы нейросети
        logits_default = self.default_head(latent).squeeze(-1)
        p_default = torch.sigmoid(logits_default)
        days_to_default = self.survival_head(latent).squeeze(-1)

        return p_default, days_to_default, attn_weights