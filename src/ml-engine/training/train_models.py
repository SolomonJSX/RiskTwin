import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import lightgbm as lgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report


def train_pipeline():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "training" / "credit_behavior_dataset.csv"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("📂 Чтение сгенерированного LLM датасета (1000 персон)...")
    df = pd.read_csv(data_path)

    # Фильтруем заемщиков строго 18+ лет
    df = df[df["age"] >= 18].copy()
    print(f"✅ Отобрано {len(df)} совершеннолетних заемщиков (18-65 лет)")

    # 23 поведенческих и финансовых признака для кредитного скоринга
    feature_cols = [
        "salary_trend_ratio_3m_vs_6m", "salary_inflow_delay_days", "inflow_source_entropy",
        "net_cashflow_margin_30d", "atm_cash_out_intensity", "credit_to_debit_transfer_ratio",
        "essential_spending_share_trend", "balance_zero_out_frequency", "mfo_gambling_tag_presence",
        "balance_check_frequency_surge", "loan_schedule_screen_dwell_time", "support_chat_keyword_velocity",
        "microloan_calculator_views", "dti_dynamic_estimate", "active_bnpl_installment_count",
        "grace_period_exhaustion_rate", "early_payment_decay_days", "median_daily_balance_7d",
        "median_daily_balance_30d", "median_daily_balance_90d", "p2p_outflow_sum_7d",
        "p2p_outflow_sum_30d", "failed_autopay_attempts_30d"
    ]

    # Преобразуем boolean колонки в float/int
    for col in ["mfo_gambling_tag_presence"]:
        if col in df.columns:
            df[col] = df[col].astype(int)

    X = df[feature_cols]
    y = df["target_default_30d"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"🚀 Обучение LightGBM Classifier на {len(X_train)} примерах (доля риска: {y.mean():.1%})...")

    # Настройка гиперпараметров LightGBM для устойчивого обобщения
    model = lgb.LGBMClassifier(
        n_estimators=150,
        learning_rate=0.04,
        max_depth=5,
        num_leaves=20,
        colsample_bytree=0.6,
        subsample=0.8,
        min_child_samples=15,
        random_state=42,
        importance_type="gain",
        verbose=-1,
    )
    model.fit(X_train, y_train)

    # Оценка качества модели
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)

    print("\n" + "=" * 60)
    print(f"🎯 МЕТРИКА ROC-AUC: {auc:.4f}")
    print("=" * 60)
    print(classification_report(y_test, (y_pred_proba >= 0.50).astype(int), target_names=["Норма", "Преддефолт"]))

    # Создание SHAP TreeExplainer на реальном обученном бустинге
    print("🧠 Создание настоящего TreeSHAP Explainer для XAI интерпретируемости...")
    explainer = shap.TreeExplainer(model)

    # Сохранение артефактов
    with open(models_dir / "early_warning_lgbm.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(models_dir / "shap_explainer.pkl", "wb") as f:
        pickle.dump(explainer, f)

    with open(models_dir / "feature_columns.pkl", "wb") as f:
        pickle.dump(feature_cols, f)

    print(f"💾 Модель и веса SHAP сохранены в: {models_dir}")
    print("🎉 Production ML пайплайн успешно обучен на данных от Ollama!")


if __name__ == "__main__":
    train_pipeline()