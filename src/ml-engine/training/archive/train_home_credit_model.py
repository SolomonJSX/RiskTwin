"""
Training Deep Dual-Tower Transactional Network & LightGBM Baseline
on 163,517 Real Home Credit Borrowers with 6.8M Payment Transactions.
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
        # x: [Batch, num_features] -> [Batch, num_features, embed_dim]
        return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)


class TransactionalCrossAttentionNet(nn.Module):
    """
    Двухбашенная нейросеть с честным Cross-Attention:
    Башня 1 (Условия кредита): параметры займа и платежеспособности
    Башня 2 (Транзакции): реальная платежная дисциплина и задержки платежей
    Cross-Attention: кредитные условия сопоставляются с транзакционной надежностью.
    """
    def __init__(self, credit_dim: int, trans_dim: int, embed_dim: int = 32, num_heads: int = 4, dropout: float = 0.2):
        super().__init__()
        self.credit_tokenizer = FeatureTokenizer(credit_dim, embed_dim)
        self.trans_tokenizer = FeatureTokenizer(trans_dim, embed_dim)

        self.credit_norm = nn.LayerNorm(embed_dim)
        self.trans_norm = nn.LayerNorm(embed_dim)

        # Cross-Attention: Кредитная башня опрашивает Транзакционную башню
        self.cross_attn = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.norm_cross = nn.LayerNorm(embed_dim)

        fusion_dim = (credit_dim + trans_dim + credit_dim) * embed_dim
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

    def forward(self, credit_x: torch.Tensor, trans_x: torch.Tensor):
        c_tok = self.credit_norm(self.credit_tokenizer(credit_x))
        t_tok = self.trans_norm(self.trans_tokenizer(trans_x))

        # Кросс-внимание
        attn_out, weights = self.cross_attn(query=c_tok, key=t_tok, value=t_tok)
        c_cross = self.norm_cross(c_tok + attn_out)

        # Объединение эмбеддингов
        flat = torch.cat([
            c_tok.flatten(start_dim=1),
            t_tok.flatten(start_dim=1),
            c_cross.flatten(start_dim=1)
        ], dim=-1)

        logits = self.head(flat).squeeze(-1)
        return logits, weights


class TabularDataset(Dataset):
    def __init__(self, credit_x: np.ndarray, trans_x: np.ndarray, y: np.ndarray):
        self.credit_x = torch.tensor(credit_x, dtype=torch.float32)
        self.trans_x = torch.tensor(trans_x, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.credit_x[idx], self.trans_x[idx], self.y[idx]


def train():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "home_credit_transactional_prepared.parquet"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("🚀 ОБУЧЕНИЕ МОДЕЛИ НА РЕАЛЬНЫХ ТРАНЗАКЦИЯХ HOME CREDIT (163 517 ЗАЕМЩИКОВ)")
    print("=" * 80)

    print(f"[*] Чтение подготовленного датасета: {data_path}")
    df = pd.read_parquet(data_path)
    print(f"[+] Всего записей: {len(df):,}")

    # 1. Разделение признаков на две башни
    credit_feature_cols = [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "dti_ratio",
        "credit_to_income_ratio",
        "age_years",
        "employment_years",
    ]

    trans_feature_cols = [
        "total_transactions",
        "avg_payment_delay_days",
        "max_payment_delay_days",
        "late_payment_count",
        "underpayment_count",
        "avg_payment_ratio",
        "total_payment_deficit",
        "total_amount_paid",
    ]

    # Категориальные признаки кодируем one-hot
    categorical_cols = ["NAME_CONTRACT_TYPE", "NAME_INCOME_TYPE", "NAME_HOUSING_TYPE"]
    df_cat = pd.get_dummies(df[categorical_cols], drop_first=True)
    all_credit_cols = credit_feature_cols + list(df_cat.columns)

    X_credit = pd.concat([df[credit_feature_cols], df_cat], axis=1).fillna(0).values.astype(np.float32)
    X_trans = df[trans_feature_cols].fillna(0).values.astype(np.float32)
    y = df["TARGET"].values.astype(np.float32)

    # 2. Train / Val / Test разбиение (70% / 15% / 15%)
    idx = np.arange(len(y))
    train_idx, test_idx = train_test_split(idx, test_size=0.15, random_state=42, stratify=y)
    train_idx, val_idx = train_test_split(train_idx, test_size=0.176, random_state=42, stratify=y[train_idx])

    # Нормализация
    scaler_credit = StandardScaler()
    scaler_trans = StandardScaler()

    X_c_train = scaler_credit.fit_transform(X_credit[train_idx])
    X_c_val = scaler_credit.transform(X_credit[val_idx])
    X_c_test = scaler_credit.transform(X_credit[test_idx])

    X_t_train = scaler_trans.fit_transform(X_trans[train_idx])
    X_t_val = scaler_trans.transform(X_trans[val_idx])
    X_t_test = scaler_trans.transform(X_trans[test_idx])

    y_train = y[train_idx]
    y_val = y[val_idx]
    y_test = y[test_idx]

    print(f"📊 Выборка: Обучение = {len(y_train):,} | Валидация = {len(y_val):,} | Тест = {len(y_test):,}")
    print(f"📌 Кредитная башня: {X_c_train.shape[1]} признаков | Транзакционная башня: {X_t_train.shape[1]} признаков")
    print(f"🎯 Доля дефолтов в тесте: {y_test.mean():.2%}")

    # 3. Даталоадеры
    train_loader = DataLoader(TabularDataset(X_c_train, X_t_train, y_train), batch_size=512, shuffle=True)
    val_loader = DataLoader(TabularDataset(X_c_val, X_t_val, y_val), batch_size=1024, shuffle=False)

    # 4. Модель и оптимизация
    model = TransactionalCrossAttentionNet(credit_dim=X_c_train.shape[1], trans_dim=X_t_train.shape[1])
    # Балансировка редкого класса дефолта через pos_weight
    pos_weight = torch.tensor([(len(y_train) - y_train.sum()) / y_train.sum()])
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1.5e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=12)

    best_val_auc = 0.0
    best_state = None

    epochs = 12
    print(f"\n🧠 Старт обучения PyTorch TransactionalCrossAttentionNet ({epochs} эпох)...")
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for bx_c, bx_t, by in train_loader:
            optimizer.zero_grad()
            logits, _ = model(bx_c, bx_t)
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
            for bx_c, bx_t, by in val_loader:
                logits, _ = model(bx_c, bx_t)
                probs = torch.sigmoid(logits)
                val_preds.extend(probs.numpy())

        val_auc = roc_auc_score(y_val, val_preds)
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            best_state = model.state_dict().copy()

        print(f"   Эпоха {epoch:02d}/{epochs:02d} | Train Loss: {train_loss:.4f} | Val ROC-AUC: {val_auc:.4f}")

    # 5. Оценка на тестовой выборке
    model.load_state_dict(best_state)
    model.eval()

    test_c_tensor = torch.tensor(X_c_test, dtype=torch.float32)
    test_t_tensor = torch.tensor(X_t_test, dtype=torch.float32)
    with torch.no_grad():
        test_logits, _ = model(test_c_tensor, test_t_tensor)
        test_probs_nn = torch.sigmoid(test_logits).numpy()

    test_auc_nn = roc_auc_score(y_test, test_probs_nn)
    test_prauc_nn = average_precision_score(y_test, test_probs_nn)
    test_preds_binary = (test_probs_nn >= 0.5).astype(int)
    test_acc_nn = accuracy_score(y_test, test_preds_binary)
    test_f1_nn = f1_score(y_test, test_preds_binary)

    # 6. LightGBM бейзлайн для сравнения
    print("\n🌲 Обучение эталонного LightGBM на объединенных признаках...")
    X_all_train = np.hstack([X_c_train, X_t_train])
    X_all_val = np.hstack([X_c_val, X_t_val])
    X_all_test = np.hstack([X_c_test, X_t_test])

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
        num_boost_round=250,
        valid_sets=[lgb_val],
        callbacks=[lgb.early_stopping(stopping_rounds=25, verbose=False)]
    )
    test_probs_lgb = gbm.predict(X_all_test)
    test_auc_lgb = roc_auc_score(y_test, test_probs_lgb)

    # 7. Вывод и сохранение результатов
    print("\n" + "=" * 80)
    print("🏆 РЕЗУЛЬТАТЫ ОБУЧЕНИЯ НА 163 517 РЕАЛЬНЫХ КЛИЕНТАХ HOME CREDIT:")
    print("=" * 80)
    print(f"  🔹 PyTorch Cross-Attention ROC-AUC : {test_auc_nn:.4f} ({test_auc_nn*100:.1f}%)")
    print(f"  🔹 PyTorch PR-AUC                  : {test_prauc_nn:.4f}")
    print(f"  🔹 PyTorch Accuracy                : {test_acc_nn:.2%}")
    print(f"  🔹 PyTorch F1-Score                : {test_f1_nn:.4f}")
    print(f"  🔹 LightGBM Benchmark ROC-AUC      : {test_auc_lgb:.4f} ({test_auc_lgb*100:.1f}%)")
    print("=" * 80)

    # Сохраняем веса и скалеры
    model_save_path = models_dir / "home_credit_transactional_model.pt"
    torch.save({
        "model_state_dict": model.state_dict(),
        "credit_dim": X_c_train.shape[1],
        "trans_dim": X_t_train.shape[1],
        "credit_cols": all_credit_cols,
        "trans_cols": trans_feature_cols,
        "test_auc": float(test_auc_nn),
    }, model_save_path)

    scalers_save_path = models_dir / "home_credit_transactional_scalers.pkl"
    with open(scalers_save_path, "wb") as f:
        pickle.dump({
            "scaler_credit": scaler_credit,
            "scaler_trans": scaler_trans,
            "credit_cols": all_credit_cols,
            "trans_cols": trans_feature_cols,
        }, f)

    metrics_save_path = models_dir / "home_credit_transactional_metrics.json"
    metrics_data = {
        "dataset_name": "Kaggle Home Credit Default Risk (163,517 borrowers, 6.8M transactions)",
        "total_borrowers": int(len(df)),
        "train_borrowers": int(len(y_train)),
        "test_borrowers": int(len(y_test)),
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
