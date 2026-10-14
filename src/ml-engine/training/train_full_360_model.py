"""
Full 360-Degree PyTorch Cross-Attention & LightGBM Training.
Trained on 163,517 real Home Credit borrowers integrating:
- Application & Bureau parameters (EXT_SOURCE scores, DTI, debts in other banks, past refusals)
- Transactional & Behavioral parameters (payment delays, ATM cash withdrawals, BNPL contracts, card utilization)
"""

import sys
import os
import json
import pickle
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score
import lightgbm as lgb


class FeatureTokenizer(nn.Module):
    def __init__(self, num_features: int, embed_dim: int):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(num_features, embed_dim) * 0.02)
        self.bias = nn.Parameter(torch.zeros(num_features, embed_dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)


class Full360CrossAttentionNet(nn.Module):
    """
    Двухбашенная глубокая сеть полного 360° цикла:
    Башня 1 (Кредит и Бюро): условия займа + скоры ПКБ + долги в других банках + отказы
    Башня 2 (Поведение и Транзакции): задержки платежей + снятие наличных + товарные рассрочки + карты
    Cross-Attention: кредитные обязательства опрашивают поведенческую дисциплину заемщика.
    """
    def __init__(self, credit_dim: int, behavior_dim: int, embed_dim: int = 32, num_heads: int = 4, dropout: float = 0.25):
        super().__init__()
        self.credit_tokenizer = FeatureTokenizer(credit_dim, embed_dim)
        self.behavior_tokenizer = FeatureTokenizer(behavior_dim, embed_dim)

        self.credit_norm = nn.LayerNorm(embed_dim)
        self.behavior_norm = nn.LayerNorm(embed_dim)

        # Cross-Attention
        self.cross_attn = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.norm_cross = nn.LayerNorm(embed_dim)

        fusion_dim = (credit_dim + behavior_dim + credit_dim) * embed_dim
        self.head = nn.Sequential(
            nn.Linear(fusion_dim, 128),
            nn.BatchNorm1d(128),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(64, 1)
        )

    def forward(self, credit_x: torch.Tensor, behavior_x: torch.Tensor):
        c_tok = self.credit_norm(self.credit_tokenizer(credit_x))
        b_tok = self.behavior_norm(self.behavior_tokenizer(behavior_x))

        # Cross-Attention: Кредит опрашивает Поведение
        attn_out, weights = self.cross_attn(query=c_tok, key=b_tok, value=b_tok)
        c_cross = self.norm_cross(c_tok + attn_out)

        flat = torch.cat([
            c_tok.flatten(start_dim=1),
            b_tok.flatten(start_dim=1),
            c_cross.flatten(start_dim=1)
        ], dim=-1)

        logits = self.head(flat).squeeze(-1)
        return logits, weights


class Tabular360Dataset(Dataset):
    def __init__(self, c_x: np.ndarray, b_x: np.ndarray, y: np.ndarray):
        self.c_x = torch.tensor(c_x, dtype=torch.float32)
        self.b_x = torch.tensor(b_x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.c_x[idx], self.b_x[idx], self.y[idx]


def train():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "home_credit_full_360_prepared.parquet"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("🚀 ОБУЧЕНИЕ 360° МОДЕЛИ НА ВСЕХ 6 ТАБЛИЦАХ HOME CREDIT (163 517 ЗАЕМЩИКОВ)")
    print("=" * 80)

    print(f"[*] Загрузка подготовленного 360° датасета: {data_path}")
    df = pd.read_parquet(data_path)
    print(f"[+] Всего записей: {len(df):,}")

    # Разделение признаков на Башню 1 (Кредит + Бюро) и Башню 2 (Поведение + Транзакции)
    credit_cols = [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "dti_ratio",
        "credit_to_income_ratio",
        "age_years",
        "employment_years",
        "EXT_SOURCE_1",
        "EXT_SOURCE_2",
        "EXT_SOURCE_3",
        "prev_app_total",
        "prev_refused_count",
        "prev_approved_count",
        "bureau_active_loans",
        "bureau_total_debt",
        "bureau_total_overdue",
        "bureau_prolong_count",
    ]

    behavior_cols = [
        "inst_total_tx",
        "inst_avg_delay_days",
        "inst_max_delay_days",
        "inst_late_count",
        "inst_underpay_count",
        "inst_total_deficit",
        "pos_active_count",
        "pos_completed_count",
        "pos_remaining_installments",
        "pos_max_dpd",
        "cc_atm_drawings_sum",
        "cc_atm_drawings_cnt",
        "cc_pos_drawings_sum",
        "cc_utilization_mean",
        "cc_max_dpd",
    ]

    # Кодирование категориальных колонок
    cat_cols = ["NAME_CONTRACT_TYPE", "NAME_INCOME_TYPE", "NAME_HOUSING_TYPE"]
    df_cat = pd.get_dummies(df[cat_cols], drop_first=True)
    all_credit_cols = credit_cols + list(df_cat.columns)

    X_credit = pd.concat([df[credit_cols], df_cat], axis=1).fillna(0).values.astype(np.float32)
    X_behavior = df[behavior_cols].fillna(0).values.astype(np.float32)
    y = df["TARGET"].values.astype(np.float32)

    # Train / Val / Test разбиение (70% / 15% / 15%)
    idx = np.arange(len(y))
    train_idx, test_idx = train_test_split(idx, test_size=0.15, random_state=42, stratify=y)
    train_idx, val_idx = train_test_split(train_idx, test_size=0.176, random_state=42, stratify=y[train_idx])

    # Нормализация
    scaler_credit = StandardScaler()
    scaler_behavior = StandardScaler()

    X_c_train = scaler_credit.fit_transform(X_credit[train_idx])
    X_c_val = scaler_credit.transform(X_credit[val_idx])
    X_c_test = scaler_credit.transform(X_credit[test_idx])

    X_b_train = scaler_behavior.fit_transform(X_behavior[train_idx])
    X_b_val = scaler_behavior.transform(X_behavior[val_idx])
    X_b_test = scaler_behavior.transform(X_behavior[test_idx])

    y_train = y[train_idx]
    y_val = y[val_idx]
    y_test = y[test_idx]

    print(f"📊 Выборка: Обучение = {len(y_train):,} | Валидация = {len(y_val):,} | Тест = {len(y_test):,}")
    print(f"📌 Башня Кредит+Бюро: {X_c_train.shape[1]} признаков | Башня Поведение: {X_b_train.shape[1]} признаков")
    print(f"🎯 Доля дефолтов в тесте: {y_test.mean():.2%}")

    # Даталоадеры
    train_loader = DataLoader(Tabular360Dataset(X_c_train, X_b_train, y_train), batch_size=512, shuffle=True)
    val_loader = DataLoader(Tabular360Dataset(X_c_val, X_b_val, y_val), batch_size=1024, shuffle=False)

    # Инициализация модели
    model = Full360CrossAttentionNet(credit_dim=X_c_train.shape[1], behavior_dim=X_b_train.shape[1])
    pos_weight = torch.tensor([(len(y_train) - y_train.sum()) / y_train.sum()])
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1.5e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=12)

    best_val_auc = 0.0
    best_state = None

    epochs = 12
    print(f"\n🧠 Старт обучения PyTorch Full360CrossAttentionNet ({epochs} эпох)...")
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for bx_c, bx_b, by in train_loader:
            optimizer.zero_grad()
            logits, _ = model(bx_c, bx_b)
            loss = criterion(logits, by)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(by)

        scheduler.step()
        train_loss = total_loss / len(y_train)

        # Валидация
        model.eval()
        val_preds = []
        with torch.no_grad():
            for bx_c, bx_b, by in val_loader:
                logits, _ = model(bx_c, bx_b)
                probs = torch.sigmoid(logits)
                val_preds.extend(probs.numpy())

        val_auc = roc_auc_score(y_val, val_preds)
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            best_state = model.state_dict().copy()

        print(f"   Эпоха {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f} | Val ROC-AUC: {val_auc:.4f}")

    # Восстановление лучших весов и тест
    model.load_state_dict(best_state)
    model.eval()

    test_c_tensor = torch.tensor(X_c_test, dtype=torch.float32)
    test_b_tensor = torch.tensor(X_b_test, dtype=torch.float32)
    with torch.no_grad():
        test_logits, _ = model(test_c_tensor, test_b_tensor)
        test_probs_nn = torch.sigmoid(test_logits).numpy()

    test_auc_nn = roc_auc_score(y_test, test_probs_nn)
    test_prauc_nn = average_precision_score(y_test, test_probs_nn)
    test_preds_binary = (test_probs_nn >= 0.5).astype(int)
    test_acc_nn = accuracy_score(y_test, test_preds_binary)
    test_f1_nn = f1_score(y_test, test_preds_binary)

    # LightGBM бейзлайн
    print("\n🌲 Обучение эталонного градиентного бустинга LightGBM на 360° признаках...")
    X_all_train = np.hstack([X_c_train, X_b_train])
    X_all_val = np.hstack([X_c_val, X_b_val])
    X_all_test = np.hstack([X_c_test, X_b_test])

    lgb_train = lgb.Dataset(X_all_train, label=y_train)
    lgb_val = lgb.Dataset(X_all_val, label=y_val, reference=lgb_train)

    lgb_params = {
        "objective": "binary",
        "metric": "auc",
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "verbose": -1,
        "random_state": 42
    }
    gbm = lgb.train(
        lgb_params,
        lgb_train,
        num_boost_round=300,
        valid_sets=[lgb_val],
        callbacks=[lgb.early_stopping(stopping_rounds=30, verbose=False)]
    )
    test_probs_lgb = gbm.predict(X_all_test)
    test_auc_lgb = roc_auc_score(y_test, test_probs_lgb)

    # Итоги
    print("\n" + "=" * 80)
    print("🏆 РЕЗУЛЬТАТЫ ОБУЧЕНИЯ 360° МОДЕЛИ (163 517 ЗАЕМЩИКОВ):")
    print("=" * 80)
    print(f"  🔹 PyTorch Full 360° Cross-Attention ROC-AUC : {test_auc_nn:.4f} ({test_auc_nn*100:.1f}%)")
    print(f"  🔹 PyTorch PR-AUC                            : {test_prauc_nn:.4f}")
    print(f"  🔹 PyTorch Accuracy                          : {test_acc_nn:.2%}")
    print(f"  🔹 PyTorch F1-Score                          : {test_f1_nn:.4f}")
    print(f"  🔹 LightGBM Benchmark ROC-AUC                : {test_auc_lgb:.4f} ({test_auc_lgb*100:.1f}%)")
    print("=" * 80)

    # Сохранение весов и метаданных
    model_save_path = models_dir / "home_credit_full_360_model.pt"
    torch.save({
        "model_state_dict": model.state_dict(),
        "credit_dim": X_c_train.shape[1],
        "behavior_dim": X_b_train.shape[1],
        "credit_cols": all_credit_cols,
        "behavior_cols": behavior_cols,
        "test_auc": float(test_auc_nn),
    }, model_save_path)

    scalers_save_path = models_dir / "home_credit_full_360_scalers.pkl"
    with open(scalers_save_path, "wb") as f:
        pickle.dump({
            "scaler_credit": scaler_credit,
            "scaler_behavior": scaler_behavior,
            "credit_cols": all_credit_cols,
            "behavior_cols": behavior_cols,
        }, f)

    metrics_save_path = models_dir / "home_credit_full_360_metrics.json"
    metrics_data = {
        "dataset_name": "Kaggle Home Credit 360-Degree (All 6 Tables Integrated)",
        "total_borrowers": int(len(df)),
        "train_borrowers": int(len(y_train)),
        "test_borrowers": int(len(y_test)),
        "features_total": int(X_c_train.shape[1] + X_b_train.shape[1]),
        "default_rate": round(float(y.mean()), 4),
        "metrics": {
            "pytorch_cross_attention_roc_auc": round(float(test_auc_nn), 4),
            "pytorch_pr_auc": round(float(test_prauc_nn), 4),
            "pytorch_accuracy": round(float(test_acc_nn), 4),
            "pytorch_f1": round(float(test_f1_nn), 4),
            "lightgbm_roc_auc": round(float(test_auc_lgb), 4),
        }
    }
    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Веса модели сохранены: {model_save_path}")
    print(f"✅ Скалеры признаков сохранены: {scalers_save_path}")
    print(f"✅ Протокол валидации сохранен: {metrics_save_path}")


if __name__ == "__main__":
    train()
