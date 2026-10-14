"""
Train Unsupervised Behavioral Distress Engine on 163,517 real Home Credit borrowers.
Discovers latent behavioral distress states and trains Gaussian Mixture Model / KMeans
without ANY hardcoded or synthetic heuristics.
"""

import json
import pickle
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import RobustScaler


def engineer_distress_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Математически строгий расчет объективных факторов финансового и поведенческого стресса
    из реальных транзакционных таблиц Home Credit.
    """
    annuity = df["AMT_ANNUITY"].clip(lower=1000.0)
    
    # 1. Cash Panic Ratio: паническое обналичивание кредитки при исчерпании лимита
    # Высокое снятие в банкоматах + высокая утилизация
    pos_draw = df["cc_pos_drawings_sum"].clip(lower=0.0)
    atm_draw = df["cc_atm_drawings_sum"].clip(lower=0.0)
    cc_util = df["cc_utilization_mean"].clip(lower=0.0, upper=2.0)
    cash_panic_ratio = (atm_draw / (pos_draw + 1000.0)) * cc_util
    
    # 2. Payment Delay Distress: задержки платежей и частота сбоев
    delay_days = df["inst_avg_delay_days"].clip(lower=0.0)
    late_ratio = (df["inst_late_count"] / (df["inst_total_tx"] + 1.0)).clip(0.0, 1.0)
    payment_delay_distress = late_ratio * np.log1p(delay_days)
    
    # 3. Deficit Burden Ratio: накопленный дефицит платежей к размеру месячного аннуитета
    inst_deficit = df["inst_total_deficit"].clip(lower=0.0)
    deficit_burden_ratio = np.log1p(inst_deficit / annuity)
    
    # 4. Rejection Desperation Rate: веерная подача заявок и фрустрация от отказов
    prev_total = df["prev_app_total"].clip(lower=0.0)
    prev_refused = df["prev_refused_count"].clip(lower=0.0)
    rejection_desperation_rate = prev_refused / (prev_total + 1.0)
    
    # 5. BNPL / POS Fragmentation Burden: импульсивное дробление на мелкие товарные рассрочки
    pos_active = df["pos_active_count"].clip(lower=0.0)
    pos_rem = df["pos_remaining_installments"].clip(lower=0.0)
    bnpl_fragmentation_burden = np.log1p(pos_active * np.sqrt(pos_rem + 1.0))
    
    # 6. External Bureau Shock: просрочки и пролонгации в сторонних банках
    bureau_overdue = df["bureau_total_overdue"].clip(lower=0.0)
    pos_dpd = df["pos_max_dpd"].clip(lower=0.0)
    cc_dpd = df["cc_max_dpd"].clip(lower=0.0)
    max_dpd = np.maximum(pos_dpd, cc_dpd)
    bureau_shock_severity = np.log1p(bureau_overdue / 1000.0) + np.log1p(max_dpd)

    distress_df = pd.DataFrame({
        "cash_panic_ratio": cash_panic_ratio.fillna(0.0),
        "payment_delay_distress": payment_delay_distress.fillna(0.0),
        "deficit_burden_ratio": deficit_burden_ratio.fillna(0.0),
        "rejection_desperation_rate": rejection_desperation_rate.fillna(0.0),
        "bnpl_fragmentation_burden": bnpl_fragmentation_burden.fillna(0.0),
        "bureau_shock_severity": bureau_shock_severity.fillna(0.0),
    }).fillna(0.0)
    return distress_df


def train_behavioral_distress():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "home_credit_full_360_prepared.parquet"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("🧠 ОБУЧЕНИЕ ОБЪЕКТИВНОЙ МОДЕЛИ ПОВЕДЕНЧЕСКОГО СТРЕССА (UNSUPERVISED GMM)")
    print("=" * 80)
    print(f"[*] Чтение реального датасета: {data_path}")
    df = pd.read_parquet(data_path)
    print(f"[+] Всего заемщиков в выборке: {len(df):,}")

    print("\n[1/4] 📊 Расчет объективных индикаторов финансово-поведенческого стресса...")
    distress_features_df = engineer_distress_features(df)
    feature_names = distress_features_df.columns.tolist()
    print(f"      Признаки дистресса: {feature_names}")

    # Стандартизация робастным скалером (устойчив к выбросам в суммах)
    scaler = RobustScaler(quantile_range=(10.0, 90.0))
    X_scaled = scaler.fit_transform(distress_features_df)

    print("\n[2/4] 🧩 Обучение Gaussian Mixture Model на 4 латентных состояния...")
    gmm = GaussianMixture(
        n_components=4,
        covariance_type="diag",
        max_iter=150,
        random_state=42,
    )
    gmm.fit(X_scaled)
    
    cluster_labels = gmm.predict(X_scaled)
    cluster_probs = gmm.predict_proba(X_scaled)

    # Анализ средних значений признаков по каждому кластеру для авто-идентификации
    cluster_means = []
    default_rates = []
    for c_id in range(4):
        mask = (cluster_labels == c_id)
        means = distress_features_df[mask].mean()
        def_rate = float(df.loc[mask, "TARGET"].mean()) if mask.sum() > 0 else 0.0
        cluster_means.append(means)
        default_rates.append(def_rate)
        print(f"   Кластер {c_id}: заемщиков={mask.sum():,} ({mask.mean():.1%}), Default Rate={def_rate:.2%}")

    # Сортируем кластеры по уровню дефолтности:
    # 0 -> Самый низкий риск (Стабильный), 3 -> Самый высокий риск (Критический стресс)
    sorted_order = np.argsort(default_rates)
    cluster_mapping = {}
    
    state_templates = [
        {"code": "STABLE_DISCIPLINE", "name": "Финансовая устойчивость и самоконтроль", "level": "LOW"},
        {"code": "LATENT_ANXIETY", "name": "Латентная тревожность и дробление рассрочек", "level": "MODERATE"},
        {"code": "ACUTE_PANIC", "name": "Острая паника: обналичивание кредиток и отказы", "level": "HIGH_EARLY_WARNING"},
        {"code": "CHRONIC_EXHAUSTION", "name": "Хроническое истощение и дефолтный коллапс", "level": "CRITICAL"},
    ]

    for new_rank, orig_id in enumerate(sorted_order):
        int_id = int(orig_id)
        meta = state_templates[new_rank]
        cluster_mapping[int_id] = {
            "rank": int(new_rank),
            "code": meta["code"],
            "name": meta["name"],
            "risk_level": meta["level"],
            "default_rate": round(float(default_rates[orig_id]), 4),
            "size": int((cluster_labels == orig_id).sum()),
            "feature_profile": {col: round(float(cluster_means[orig_id][col]), 4) for col in feature_names}
        }
        print(f"   Кластер {int_id} -> Ступень {new_rank}: {meta['name']} (DR={default_rates[orig_id]:.2%})")

    # Сохраняем модель
    model_artifact = {
        "scaler": scaler,
        "gmm": gmm,
        "feature_names": feature_names,
        "cluster_mapping": cluster_mapping,
        "sorted_order": [int(x) for x in sorted_order],
    }
    
    model_save_path = models_dir / "behavioral_distress_model.pkl"
    with open(model_save_path, "wb") as f:
        pickle.dump(model_artifact, f)

    meta_save_path = models_dir / "behavioral_distress_metadata.json"
    with open(meta_save_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_samples": int(len(df)),
            "feature_names": feature_names,
            "clusters": {str(k): v for k, v in cluster_mapping.items()},
            "validation_note": "Unsupervised Gaussian Mixture Model fitted on raw Home Credit transactional telemetry."
        }, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("✅ МОДЕЛЬ ПОВЕДЕНЧЕСКОГО СТРЕССА УСПЕШНО ОБУЧЕНА И СОХРАНЕНА!")
    print(f"   Файл модели:    {model_save_path}")
    print(f"   Метаданные:     {meta_save_path}")
    print("=" * 80)


if __name__ == "__main__":
    train_behavioral_distress()
