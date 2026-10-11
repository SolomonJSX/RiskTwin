import pickle
from pathlib import Path
import numpy as np
import pandas as pd
import lightgbm as lgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report


def train_psycho_life_pipeline():
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "training" / "psycho_life_dataset.csv"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    print("📂 Чтение сгенерированного Psycho-Life датасета (1000 заемщиков)...")
    df = pd.read_csv(data_path)

    # 15 ключевых психоэмоциональных и поведенческих признаков
    feature_cols = [
        "pharmacy_antidepressant_share",
        "clinical_therapy_spending_30d",
        "nighttime_alcohol_spend_share",
        "gambling_escapism_outflow",
        "self_care_drop_rate",
        "sleep_disruption_night_orders",
        "night_dbo_login_frequency",
        "dwell_time_repayment_screen",
        "balance_check_anxiety_index",
        "alimony_burden_ratio",
        "p2p_borrowing_from_friends_count",
        "utility_debt_months",
        "salary_trend_post_crisis",
        "dti_dynamic_estimate",
        "age",
    ]

    X = df[feature_cols]
    y = df["target_depression_crisis"]  # Целевая переменная: глубокий психоэмоциональный кризис

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"🚀 Обучение Psycho-Life Crisis Classifier на {len(X_train)} заемщиках...")

    # Настройка LightGBM классификатора с регуляризацией
    model = lgb.LGBMClassifier(
        n_estimators=120,
        learning_rate=0.04,
        max_depth=4,
        num_leaves=15,
        colsample_bytree=0.7,
        subsample=0.8,
        min_child_samples=15,
        random_state=42,
        importance_type="gain",
        verbose=-1,
    )
    model.fit(X_train, y_train)

    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)

    print("\n" + "=" * 65)
    print(f"🎯 МЕТРИКА ROC-AUC ДЕТЕКЦИИ ПСИХОЛОГИЧЕСКОГО КРИЗИСА: {auc:.4f}")
    print("=" * 65)
    print(classification_report(y_test, (y_pred_proba >= 0.50).astype(int), target_names=["Гармония", "Кризис/Депрессия"]))

    # Создание специализированного TreeSHAP Explainer для объяснения личных причин
    print("🧠 Создание TreeSHAP Explainer для психологической интерпретируемости...")
    explainer = shap.TreeExplainer(model)

    # Сохранение обученной модели и артефактов
    with open(models_dir / "psycho_life_lgbm.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(models_dir / "psycho_shap_explainer.pkl", "wb") as f:
        pickle.dump(explainer, f)

    with open(models_dir / "psycho_feature_columns.pkl", "wb") as f:
        pickle.dump(feature_cols, f)

    print(f"💾 Модель Psycho-Life и веса SHAP сохранены в: {models_dir}")
    print("🎉 Production ML модель психоэмоционального анализа успешно обучена!")


if __name__ == "__main__":
    train_psycho_life_pipeline()
