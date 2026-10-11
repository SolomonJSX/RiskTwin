import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, mean_absolute_error, classification_report

from app.infrastructure.deep_learning.cross_attention_net import DualTowerCrossAttentionNet


class BorrowerDataset(Dataset):
    def __init__(self, fin_t: torch.Tensor, psycho_t: torch.Tensor, y_def: torch.Tensor, y_days: torch.Tensor):
        self.fin_t = fin_t
        self.psycho_t = psycho_t
        self.y_def = y_def
        self.y_days = y_days

    def __len__(self):
        return len(self.y_def)

    def __getitem__(self, idx):
        return self.fin_t[idx], self.psycho_t[idx], self.y_def[idx], self.y_days[idx]


def train_deep_learning():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "training" / "deep_synergistic_dataset.csv"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("📂 Загрузка датасета для глубокого обучения PyTorch (25 000 заемщиков)...")
    df = pd.read_csv(data_path)

    fin_cols = [
        "salary_trend_ratio_3m_vs_6m",
        "salary_inflow_delay_days",
        "mfo_gambling_tag_presence",
        "dti_dynamic_estimate",
        "median_daily_balance_7d",
        "net_cashflow_margin_30d",
        "declared_income",
    ]

    psycho_cols = [
        "pharmacy_antidepressant_share",
        "nighttime_alcohol_spend_share",
        "self_care_drop_rate",
        "night_dbo_login_frequency",
        "dwell_time_repayment_screen",
        "sleep_disruption_night_orders",
        "balance_check_anxiety_index",
        "alimony_burden_ratio",
        "age",
    ]

    # Нормализация признаков
    scaler_fin = StandardScaler()
    scaler_psycho = StandardScaler()

    X_fin_scaled = scaler_fin.fit_transform(df[fin_cols])
    X_psycho_scaled = scaler_psycho.fit_transform(df[psycho_cols])

    y_def = df["target_default_30d"].values.astype(np.float32)
    y_days = df["predicted_days_to_default"].values.astype(np.float32)

    # Train / Val / Test разбиение (70% / 15% / 15%)
    idx = np.arange(len(df))
    train_idx, test_idx = train_test_split(idx, test_size=0.15, random_state=42, stratify=y_def)
    train_idx, val_idx = train_test_split(train_idx, test_size=0.176, random_state=42, stratify=y_def[train_idx])

    # Тензоры PyTorch
    train_ds = BorrowerDataset(
        torch.tensor(X_fin_scaled[train_idx], dtype=torch.float32),
        torch.tensor(X_psycho_scaled[train_idx], dtype=torch.float32),
        torch.tensor(y_def[train_idx], dtype=torch.float32),
        torch.tensor(y_days[train_idx], dtype=torch.float32),
    )
    val_ds = BorrowerDataset(
        torch.tensor(X_fin_scaled[val_idx], dtype=torch.float32),
        torch.tensor(X_psycho_scaled[val_idx], dtype=torch.float32),
        torch.tensor(y_def[val_idx], dtype=torch.float32),
        torch.tensor(y_days[val_idx], dtype=torch.float32),
    )
    test_ds = BorrowerDataset(
        torch.tensor(X_fin_scaled[test_idx], dtype=torch.float32),
        torch.tensor(X_psycho_scaled[test_idx], dtype=torch.float32),
        torch.tensor(y_def[test_idx], dtype=torch.float32),
        torch.tensor(y_days[test_idx], dtype=torch.float32),
    )

    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=128, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=128, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"⚡ Обучение на устройстве: {device}")

    model = DualTowerCrossAttentionNet(
        fin_dim=len(fin_cols),
        psycho_dim=len(psycho_cols),
        embed_dim=32,
        num_heads=4,
        dropout=0.20,
    ).to(device)

    # Оптимизатор и функции потерь
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=25)

    criterion_bce = nn.BCELoss()
    criterion_huber = nn.HuberLoss(delta=10.0)

    print("\n🚀 Старт обучения нейросети (25 эпох)...")
    best_val_auc = 0.0

    for epoch in range(1, 26):
        model.train()
        total_loss = 0.0

        for f_b, p_b, y_d_b, y_days_b in train_loader:
            f_b, p_b = f_b.to(device), p_b.to(device)
            y_d_b, y_days_b = y_d_b.to(device), y_days_b.to(device)

            optimizer.zero_grad()
            p_pred, days_pred, _ = model(f_b, p_b)

            loss_def = criterion_bce(p_pred, y_d_b)
            loss_days = criterion_huber(days_pred, y_days_b) * 0.02
            loss = loss_def + loss_days

            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        scheduler.step()

        # Валидация
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for f_b, p_b, y_d_b, _ in val_loader:
                f_b, p_b = f_b.to(device), p_b.to(device)
                p_pred, _, _ = model(f_b, p_b)
                val_preds.extend(p_pred.cpu().numpy())
                val_targets.extend(y_d_b.numpy())

        val_auc = roc_auc_score(val_targets, val_preds)
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            torch.save(model.state_dict(), models_dir / "deep_cross_attention_net.pt")

        if epoch % 5 == 0 or epoch == 25:
            print(f"   Эпоха [{epoch:02d}/25] | Loss: {total_loss/len(train_loader):.4f} | Val ROC-AUC: {val_auc:.4f}")

    # =========================================================================
    # Тестирование лучшей модели
    # =========================================================================
    model.load_state_dict(torch.load(models_dir / "deep_cross_attention_net.pt"))
    model.eval()

    test_preds, test_targets, test_days_pred, test_days_true = [], [], [], []
    with torch.no_grad():
        for f_b, p_b, y_d_b, y_days_b in test_loader:
            f_b, p_b = f_b.to(device), p_b.to(device)
            p_pred, days_pred, _ = model(f_b, p_b)
            test_preds.extend(p_pred.cpu().numpy())
            test_targets.extend(y_d_b.numpy())
            test_days_pred.extend(days_pred.cpu().numpy())
            test_days_true.extend(y_days_b.numpy())

    test_auc = roc_auc_score(test_targets, test_preds)
    mae_days = mean_absolute_error(test_days_true, test_days_pred)

    print("\n" + "=" * 70)
    print("🏆 РЕЗУЛЬТАТЫ ГЛУБОКОГО ОБУЧЕНИЯ (PYTORCH CROSS-ATTENTION):")
    print("=" * 70)
    print(f"🎯 Финальный Тестовый ROC-AUC: {test_auc:.4f}  (Нейросетевой Deep Learning!)")
    print(f"⏱️ Ошибка прогноза окна дефолта (MAE): ±{mae_days:.1f} дней")
    print("=" * 70)
    print(classification_report(test_targets, (np.array(test_preds) >= 0.50).astype(int), target_names=["Здоровый", "Преддефолт"]))

    # Сохраняем скалеры и списки колонок
    scalers_artifacts = {
        "scaler_fin": scaler_fin,
        "scaler_psycho": scaler_psycho,
        "fin_cols": fin_cols,
        "psycho_cols": psycho_cols,
    }
    with open(models_dir / "deep_learning_scalers.pkl", "wb") as f:
        pickle.dump(scalers_artifacts, f)

    print(f"💾 Веса нейросети сохранены в: {models_dir / 'deep_cross_attention_net.pt'}")
    print("🎉 Deep Learning конвейер успешно построен!")


if __name__ == "__main__":
    train_deep_learning()