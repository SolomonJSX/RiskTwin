import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import lightgbm as lgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, brier_score_loss, classification_report


def train_deep_multimodal_ensemble():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "training" / "deep_synergistic_dataset.csv"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("📂 Чтение глубокого синергетического датасета (2 500 заемщиков)...")
    df = pd.read_csv(data_path)

    # 1. Признаки финансового домена (Financial Expert)
    fin_features = [
        "salary_trend_ratio_3m_vs_6m",
        "salary_inflow_delay_days",
        "mfo_gambling_tag_presence",
        "dti_dynamic_estimate",
        "median_daily_balance_7d",
        "net_cashflow_margin_30d",
        "declared_income",
    ]

    # 2. Признаки психоэмоционального домена (Psycho-Life Expert)
    psycho_features = [
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

    y_default = df["target_default_30d"]
    y_days = df["predicted_days_to_default"]

    # Разделение на Train (70%), Stacking-Validation (15%) и Final Test (15%)
    X_train_full, X_test, y_train_full, y_test = train_test_split(
        df, y_default, test_size=0.15, random_state=42, stratify=y_default
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_full, y_train_full, test_size=0.20, random_state=42, stratify=y_train_full
    )

    print(f"🚀 Обучение Базовых Экспертов (Слой 1) на {len(X_train)} заемщиках...")

    # =========================================================================
    # СЛОЙ 1, МОДЕЛЬ A: Финансовый эксперт (Financial LightGBM)
    # =========================================================================
    fin_model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        num_leaves=12,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1,
    )
    fin_model.fit(X_train[fin_features], y_train)
    p_fin_val = fin_model.predict_proba(X_val[fin_features])[:, 1]
    p_fin_test = fin_model.predict_proba(X_test[fin_features])[:, 1]
    print(f"   [Эксперт А: Финансы] Валидационный ROC-AUC: {roc_auc_score(y_val, p_fin_val):.4f}")

    # =========================================================================
    # СЛОЙ 1, МОДЕЛЬ B: Психоэмоциональный эксперт (Psycho-Life LightGBM)
    # =========================================================================
    psycho_model = lgb.LGBMClassifier(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=4,
        num_leaves=12,
        colsample_bytree=0.8,
        random_state=42,
        verbose=-1,
    )
    psycho_model.fit(X_train[psycho_features], y_train)
    p_psycho_val = psycho_model.predict_proba(X_val[psycho_features])[:, 1]
    p_psycho_test = psycho_model.predict_proba(X_test[psycho_features])[:, 1]
    print(f"   [Эксперт B: Психология] Валидационный ROC-AUC: {roc_auc_score(y_val, p_psycho_val):.4f}")

    # =========================================================================
    # СЛОЙ 1, МОДЕЛЬ C: Модель выживаемости (Survival Days Regressor)
    # =========================================================================
    survival_model = lgb.LGBMRegressor(
        n_estimators=80,
        learning_rate=0.06,
        max_depth=4,
        num_leaves=12,
        random_state=42,
        verbose=-1,
    )
    all_features = fin_features + psycho_features
    survival_model.fit(X_train_full[all_features], y_days.loc[X_train_full.index])

    # =========================================================================
    # СЛОЙ 2: Мета-слой синергии (Synergy Stacking Meta-Learner)
    # Формируем нелинейный синергетический вектор: [P_fin, P_psycho, P_fin * P_psycho]
    # =========================================================================
    def build_meta_features(p_f: np.ndarray, p_p: np.ndarray) -> np.ndarray:
        synergy_cross = p_f * p_p  # Произведение вероятностей (наложение кризисов)
        diff_spread = np.abs(p_f - p_p) # Расхождение оценок
        return np.column_stack([p_f, p_p, synergy_cross, diff_spread])

    X_meta_val = build_meta_features(p_fin_val, p_psycho_val)
    X_meta_test = build_meta_features(p_fin_test, p_psycho_test)

    print("\n🧠 Обучение Мета-слоя синергии (Слой 2: Stacking Meta-Learner)...")
    base_meta = LogisticRegression(C=1.5, random_state=42)
    meta_learner = CalibratedClassifierCV(estimator=base_meta, method="sigmoid", cv=3)
    meta_learner.fit(X_meta_val, y_val)

    # Итоговая калиброванная оценка на тестовой выборке
    final_p_test = meta_learner.predict_proba(X_meta_test)[:, 1]
    final_auc = roc_auc_score(y_test, final_p_test)
    final_brier = brier_score_loss(y_test, final_p_test)

    print("\n" + "=" * 70)
    print("🏆 РЕЗУЛЬТАТЫ ГЛУБОКОГО СИНЕРГЕТИЧЕСКОГО АНСАМБЛЯ:")
    print("=" * 70)
    print(f"🎯 Итоговый ROC-AUC (Test): {final_auc:.4f}  (Реалистичный банковский бенчмарк!)")
    print(f"📉 Brier Score (Калибровка вероятности): {final_brier:.4f} (Чем ближе к 0, тем точнее вероятность)")
    print("=" * 70)
    print(classification_report(y_test, (final_p_test >= 0.50).astype(int), target_names=["Здоровый", "Преддефолт"]))

    # =========================================================================
    # XAI: TreeSHAP для интерпретируемости каждого домена
    # =========================================================================
    print("🔍 Инициализация мультимодальных TreeSHAP эксплейнеров...")
    fin_explainer = shap.TreeExplainer(fin_model)
    psycho_explainer = shap.TreeExplainer(psycho_model)

    # Сохранение артефактов индустриального ансамбля
    ensemble_artifacts = {
        "fin_model": fin_model,
        "fin_features": fin_features,
        "fin_explainer": fin_explainer,
        "psycho_model": psycho_model,
        "psycho_features": psycho_features,
        "psycho_explainer": psycho_explainer,
        "meta_learner": meta_learner,
        "survival_model": survival_model,
        "all_features": all_features,
    }

    with open(models_dir / "deep_multimodal_ensemble.pkl", "wb") as f:
        pickle.dump(ensemble_artifacts, f)

    print(f"\n💾 Полный ансамбль сохранен в: {models_dir / 'deep_multimodal_ensemble.pkl'}")
    print("🎉 Высокоточная enterprise-архитектура готова!")


if __name__ == "__main__":
    train_deep_multimodal_ensemble()
