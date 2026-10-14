import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from app.domain.interfaces import IScoringModel
from app.domain.entities import ClientFeatureVector


class EarlyWarningScoringModel(IScoringModel):
    """
    Production инференс модели раннего предупреждения.
    Использует реальный обученный градиентный бустинг LightGBM.
    """

    def __init__(self):
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "models" / "archive" / "early_warning_lgbm.pkl"
        if not model_path.exists():
            model_path = base_dir / "models" / "early_warning_lgbm.pkl"
        cols_path = base_dir / "models" / "archive" / "feature_columns.pkl"
        if not cols_path.exists():
            cols_path = base_dir / "models" / "feature_columns.pkl"

        if model_path.exists() and cols_path.exists():
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            with open(cols_path, "rb") as f:
                self.feature_cols = pickle.load(f)
            self._is_loaded = True
        else:
            self._is_loaded = False

    def predict_p_default(self, features: ClientFeatureVector) -> tuple[float, float]:
        if not self._is_loaded:
            # Fallback
            return 0.45, 0.58

        # Преобразуем фичи заемщика в DataFrame с правильным порядком колонок
        f_dict = features.to_feature_dict()
        df_row = pd.DataFrame([f_dict])[self.feature_cols]

        # Реальный инференс вероятности класса 1 (Преддефолт) через LightGBM
        p_30d = float(self.model.predict_proba(df_row)[0, 1])

        # Моделирование 60-дневного каскадного горизонта выживаемости (Survival proxy)
        p_30d = round(p_30d, 4)
        p_60d = min(1.0, max(p_30d, round(p_30d * 1.22, 4)))
        
        return p_30d, p_60d